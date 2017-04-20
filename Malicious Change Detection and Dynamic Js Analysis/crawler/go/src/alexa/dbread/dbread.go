package main

import (
	"encoding/json"
	"github.com/boltdb/bolt"
	"goalexa/crawler"
	"log"
	"io/ioutil"
)

const openMode = 0644

func readFromDb() {
	log.Println("db convertion begins...\n")
	db := openDB("../../../../db_dump/12-04-2017-07-46-02.db")
	defer db.Close()
	//var crawlObjects []crawler.Result
	db.View(func(tx *bolt.Tx) error {
		b := tx.Bucket([]byte("crawledSites"))
		b.ForEach(func(k, v []byte) error {
			var res crawler.Result
			err := json.Unmarshal(v, &res)
			if err != nil {
				log.Println("error", err)
			}
			//crawlObjects = append(crawlObjects, res)
			return nil
		})
		return nil
	})
	//sort.Sort(crawler.ByRank(crawlObjects))
	//sort.Slice(crawlObjects[:], func(i, j int) bool{
	//	return strconv.Atoi(crawlObjects[i].Rank) < strconv.Atoi(crawlObjects[j].Rank)
	//})
	b, err := json.Marshal(crawlObjects)
	if err != nil {
		log.Println(err)
	}
	err = ioutil.WriteFile("temp.json", b, openMode)
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
