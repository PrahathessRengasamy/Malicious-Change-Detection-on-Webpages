package main

import (
	"encoding/json"
	"github.com/boltdb/bolt"
	"goalexa/crawler"
	"io/ioutil"
	"log"
	"os"
	"sort"
)

const openMode = 0644

func readFromDb() {
	log.Println("db conversion begins...\n")
	filename := "./db_dump/" + os.Args[1]
	json_filename := os.Args[2] + ".json"
	db := openDB(filename)
	defer db.Close()
	count := 0
	var crawlObjects []crawler.Result
	f, e := os.Create("logged_sites.txt")
	if e != nil {
		log.Println(e)
	}
	s := ""
	db.View(func(tx *bolt.Tx) error {
		b := tx.Bucket([]byte("crawledSites"))
		b.ForEach(func(k, v []byte) error {
			var res crawler.Result
			err := json.Unmarshal(v, &res)
			if err != nil {
				log.Println("error", err)
			}
			count += 1
			crawlObjects = append(crawlObjects, res)
			s += res.Rank + "," + res.URL + "\n"
			log.Println(count)
			/*
			if count == 37353 {
				sort.Sort(crawler.ByRank(crawlObjects))
				b, err := json.Marshal(crawlObjects)
				if err != nil {
					log.Println(err)
				}
				f.WriteString(s)
				f.Sync()
				err = ioutil.WriteFile(json_filename, b, openMode)
				log.Println("Converted all sites into json\n")
				os.Exit(1)
			}
			*/
			return nil
		})
		return nil
	})
				sort.Sort(crawler.ByRank(crawlObjects))
				b, err := json.Marshal(crawlObjects)
				if err != nil {
					log.Println(err)
				}
				f.WriteString(s)
				f.Sync()
				err = ioutil.WriteFile(json_filename, b, openMode)
				log.Println("Converted all sites into json\n")
}

func openDB(name string) *bolt.DB {
	db, err := bolt.Open(name, openMode, nil)
	if err != nil {
		log.Fatalln("error opening db:", err)
	}
	return db
}

func main() {
	readFromDb()
}
