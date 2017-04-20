// Created by Nagendra Posani
// Created: Feb 15, 2017
// Start crawling the Alexa 1M sites.

package main 

import(
	"log"
	"os"
	"os/signal"
	"runtime"
	"time"
	"encoding/json"

	"github.com/boltdb/bolt"
	"github.com/cheggaaa/pb"
	"github.com/codegangsta/cli"
	"goalexa/crawler"
)

func crawlSites(c *cli.Context){
	level := 1 //c.Int("level") default 1
	jobs := c.Int("jobs")
	skip := c.Int("skip")

	// verify args
	if level < 1 || level > 3 {
		log.Fatalln("Invalid deepness level, value is out of range")
	}
	if jobs < 1 || jobs > 512 {
		log.Fatalln("Invalid threads number, value is out of range")
	}
	if skip < 0 {
		log.Fatalln("Invalid skip number, value is less than 0")
	}
	// open resources
	db := openDB(c.String("db"))
	defer db.Close()
	out := openDB(c.String("out"))
	defer out.Close()

	// setup runtime performance
	nCPU := runtime.NumCPU()
	runtime.GOMAXPROCS(nCPU * 2)
	log.Printf("Crawl started on %d cores, jobs: %d, deepness: %d", nCPU, jobs, level)

	// crawler init
	resultsChan := make(chan *crawler.Result, processBuffer)
	errorsChan := make(chan struct{}, processBuffer)
	cr := crawler.New(db, &crawler.Config{
		Jobs:     jobs,
		Level:    level,
	})

	// bar setup
	bar := pb.New64(sitesNum - int64(skip))
	bar.SetRefreshRate(time.Second)
	bar.ShowTimeLeft = true
	bar.ShowSpeed = true
	bar.Start()
	cr.OnProgress = bar.Increment
	defer bar.FinishPrint("All sites have been crawled.")

	// result processing routine
	go func() {
		for result := range resultsChan {
			if err := writeResults(out, result); err != nil {
				//log.Println("error saving result:", err)
			}
		}
	}()
	// errors processing routine
	var errCounter int
	go func() {
		for _ = range errorsChan {
			errCounter++
		}
	}()
	// interrupt watcher
	exitChan := make(chan os.Signal, 1)
	signal.Notify(exitChan, os.Interrupt)
	go func() {
		<-exitChan
		log.Println("Errors total:", errCounter)
		os.Exit(0)
	}()

	// begin crawling
	if err := cr.Crawl(resultsChan, errorsChan, 0); err != nil {
		log.Fatalln("unable to start crawling:", err)
	}
	log.Println("Errors total:", errCounter)
}

func writeResults(out *bolt.DB, res *crawler.Result) error {
	tx, err := out.Begin(true)
	if err != nil {
		return err
	}
	bucket, err := tx.CreateBucketIfNotExists([]byte("crawledSites"))
	if err != nil {
		return err
	}
	log.Println("db write", res.Rank)
	encoded, err := json.Marshal(res)
	bucket.Put([]byte(res.Rank), encoded)
	return tx.Commit()
}
