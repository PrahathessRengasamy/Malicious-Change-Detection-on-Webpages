package main 

import (
	"log"
	"runtime"
	"time"
	
	"github.com/codegangsta/cli"
)

var processes = runtime.NumCPU() * 2
var processBuffer = 1284 * processes

const sitesNum int64 = 100

var app = cli.NewApp()

func init() {
	var currentDB = time.Now().Format("02-01-2006-15-04-05") + ".db"
	log.SetFlags(log.Lshortfile)

	app.Name = "crawl"
	app.Usage = "An utility for fetching and parsing Alexa Top-1M sites in parallel mode."
	app.Version = "1.0"
	app.Commands = []cli.Command{
		{
			Name:   "cache",
			Action: loadSites,
			Usage:  "Caches the list of domains to crawl",
			Flags: []cli.Flag{
				cli.StringFlag{Name: "db", Value: "sites.db", Usage: "A path to DB with cached domains"},
				cli.StringFlag{Name: "csv", Value: "top-1m.csv.gz", Usage: "A csv file with domains list in format `rank,domain`"},
			},
		},
		{
			Name:   "start",
			Action: crawlSites,
			Usage:  "Start crawling the cached sites and check against some patterns",
			Flags: []cli.Flag{
				cli.StringFlag{Name: "db", Value: "sites.db", Usage: "A path to DB with cached domains"},
				cli.StringFlag{Name: "out, o", Value: currentDB, Usage: "A file to output the results to"},
				cli.IntFlag{Name: "level, l", Value: 1, Usage: "How deeply the crawler should go (1-3)"},
				cli.IntFlag{Name: "jobs, j", Value: 100, Usage: "Maximum parallel jobs allowed (1-64)"},
				cli.IntFlag{Name: "skip, s", Usage: "Skips the defined number of top-positions"},
			},
		},
	}
}

func main() {
	app.RunAndExitOnError()
}
