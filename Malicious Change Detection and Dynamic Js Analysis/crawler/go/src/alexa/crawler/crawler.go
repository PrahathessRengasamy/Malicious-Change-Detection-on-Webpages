// Created by Nagendra Posani
// Date: Feb 15, 2017
// Crawler package crawls a given URI

package crawler

import (
	"bytes"
	"log"
	"fmt"
	"net/http"
	"errors"
	"runtime"
	"strconv"
	"strings"
	"time"
	"io/ioutil"

	"github.com/rakyll/coop"
	"github.com/boltdb/bolt"
//	"github.com/fern4lvarez/go-metainspector/metainspector"	
)


var processes = runtime.NumCPU() * 2
var processBuffer = 128 * processes

var BucketSites = []byte("sites")

const connectionTimeout = time.Second * 10

type Config struct{
	Jobs int
	Level int
}

type Crawler struct{
	OnProgress func() int

	db *bolt.DB 
	config *Config
	uriChan chan string
}

type Result struct{
	Rank 		string
	URL         string
	Host 		string
	Title       string
	Description string
	Body 		string
	Language 	string
	Links		[]string
	Headers		map[string][]string
	LastModified []string
}

type ByRank []Result
func (a ByRank) Len() int { return len(a)}
func (a ByRank) Swap(i,j int) { a[i], a[j] = a[j], a[i] }
func (a ByRank) Less(i, j int) bool { 
	it, ie := strconv.Atoi(a[i].Rank); 
	if ie != nil { 
		log.Println(ie)
		return false
	}
	jt, je := strconv.Atoi(a[j].Rank)
	if je != nil {
		log.Println(je)
		return false
	} 
	return it < jt
}


func (r Result) String() string {
        return fmt.Sprintf("Rank: %s\t Host: %s ", r.Rank, r.URL)
}

func New(db *bolt.DB, config *Config) *Crawler{
	return &Crawler{db: db, config: config,}
}

func (cr *Crawler) Crawl(resultChan chan<-*Result, errorChan chan<-struct{}, skip int) error{
	cr.uriChan = make(chan string, processBuffer)
	skipB := strconv.AppendInt([]byte{}, int64(skip), 10)
	if err := cr.checkBucket(BucketSites); err != nil {
		return err
	}

	// fill the pool of URLs
	go func() {
		cr.db.View(func(tx *bolt.Tx) error {
			b := tx.Bucket(BucketSites)
			b.ForEach(func(k, v []byte) error {
				if bytesLess(k, skipB) {
					return nil
				}
				kv := string(k) + ":" + string(v)
				cr.uriChan <- kv
				return nil
			})
			return nil
		})
		close(cr.uriChan)
	}()

	process := func() {
		for uri := range cr.uriChan {
			if cr.OnProgress != nil {
				cr.OnProgress()
			}
			result, err := cr.crawlURI(uri)
			if err != nil {
				errorChan <- struct{}{}
				continue
			}
			resultChan <- result
		}
	}

	// run processing jobs
	<-coop.Replicate(cr.config.Jobs, process)
	close(resultChan)
	close(errorChan)

return nil
}

func (cr *Crawler) crawlURI(uri string) (result *Result, err error) {
	url := strings.Split(uri,":")
	//mi, err := metainspector.New(url[1])
	//if err != nil {
	//	log.Println("1:",err)
	//	return nil, err
	//}
	resp, err := http.Get("http://" + url[1])
	if err != nil{
		log.Println("2:",err)
		return nil, err
	}
	resData, err := ioutil.ReadAll(resp.Body)
	if err != nil{
		log.Println("3:",err)
	}
	body := string(resData)
	headers := resp.Header
	result = &Result{
		Rank:		 url[0],
		URL:         url[1],
		//Host: 		 mi.Host(),
		//Title:       mi.Title(),
		//Description: mi.Description(),
		Body:		 body,
		//Language:    mi.Language(),
		//Links: 		 mi.Links(),
		Headers: 	 headers,
		LastModified: headers["Last-Modified"],
	}
	log.Print(result)
	return
}

func (cr *Crawler) checkBucket(name []byte) error {
	return cr.db.Update(func(tx *bolt.Tx) error {
		if b := tx.Bucket(name); b == nil {
			return errors.New("no such bucket: " + string(name))
		}
		return nil
	})
}

// bytesLess return true iff a < b.
func bytesLess(a, b []byte) bool {
	return bytes.Compare(a, b) < 0
}
