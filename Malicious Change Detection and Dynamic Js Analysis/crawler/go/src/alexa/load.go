// Created by Nagendra Posani
// Date: Feb 15, 2017
// Loads sites to the DB

package main

import (
	"compress/gzip"
	"encoding/csv"
	"io"
	"log"
	"os"
	"time"

	"./crawler"
	"github.com/boltdb/bolt"
	"github.com/cheggaaa/pb"
	"github.com/codegangsta/cli"
)

const openMode = 0644

func loadSites(c *cli.Context){
	db := openDB(c.String("db"))
	defer db.Close()

	file, err := os.Open(c.String("csv"))
	if err != nil {
		log.Fatalln(err)
	}
	defer file.Close()
	gr, err := gzip.NewReader(file)
	if err != nil {
		log.Fatalln(err)
	}
	data := csv.NewReader(gr)
	data.FieldsPerRecord = 2

	bar := pb.New64(sitesNum)
	bar.SetRefreshRate(time.Second)
	bar.ShowTimeLeft = true
	bar.ShowSpeed = true
	defer bar.FinishPrint("All sites have been cached.")

	if err := loadData(db, data, bar); err != nil {
		log.Fatalln(err)
	}
}

func loadData(db *bolt.DB, data *csv.Reader, bar *pb.ProgressBar) error {
	tx, err := db.Begin(true)
	if err != nil {
		return err
	}
	bucket, err := tx.CreateBucketIfNotExists(crawler.BucketSites)
	if err != nil {
		return err
	}
	bar.Start()
	for {
		fields, err := data.Read()
		if err != nil {
			if err == io.EOF {
				break // end of data
			}
			return err
		}
		if err := bucket.Put([]byte(fields[0]), []byte(fields[1])); err != nil {
			return err
		}
		// site added
		current := bar.Increment()
		if current%10000 == 0 {
			if err := tx.Commit(); err != nil {
				return err
			}
			tx, err = db.Begin(true)
			if err != nil {
				return err
			}
			bucket = tx.Bucket([]byte("sites"))
		}
	}
	return tx.Commit()
}


func openDB(name string) *bolt.DB {
	db, err := bolt.Open(name, openMode, nil)
	if err != nil {
		log.Fatalln("error opening db:", err)
	}
	return db
}
