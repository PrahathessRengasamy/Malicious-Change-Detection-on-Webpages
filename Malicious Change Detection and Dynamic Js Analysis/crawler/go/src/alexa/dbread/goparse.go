package main

import (
	"fmt"
	"golang.org/x/net/html"
	"io/ioutil"
	"strings"
)

func ParseHTML(b string) string {
	var script []string
	z := html.NewTokenizer(strings.NewReader(b))
	for {
		tt := z.Next()

		switch tt {
		case html.ErrorToken:
			return strings.Join(script[:], "\n")

		case html.StartTagToken:
			t := z.Token()

			isScript := t.Data == "script"
			if !isScript {
				continue
			}
			if z.Next() == html.TextToken {
				sc := z.Token().Data
				script = append(script, sc)
			}
		}
	}
}
