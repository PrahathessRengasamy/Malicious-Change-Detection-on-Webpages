package main

import (
	"fmt"
	"log"
	"io"
	"os"
	"bufio"
	"strings"
	"encoding/csv"
	"sort"
)

var line_line         int = 0;
var line_prefix_start int = 1;
var line_prefix_end   int = 2;
var line_other        int = 3;

type MatchLine struct {
    prefix string
    line   string
    weight string
}
/*{
}
]
string: string,
string: string
string: boolean
string: [
string: {
*/

func extract(r_ast *bufio.Reader, pw *csv.Writer, con string, tabs string){
	cur := con;
	line, err := r_ast.ReadString('\n');
	for ;err != io.EOF; {
		_ = err;
		line = strings.Trim(line, " \t\r\n");
		if (strings.Contains(line,"{")){
			extract(r_ast, pw, cur, tabs + "\t");
		} else if strings.Contains(line, "}") {
			return;
		} else if len(line) <= 2 {
		} else {
			pos := strings.Index(line,":");
			s1 := strings.Trim(line[0:pos], "\"");
			s2 := strings.Trim(line[pos+1:], " ,\"");
			
			if (strings.Compare(s1,"type") == 0){
				pw.Write([]string{con, s2});
				
				//fmt.Printf("%v\n", err2);
				//fmt.Printf("%s\t%s\n", con, s2);
				cur = s2;
			}
		}
		line, err = r_ast.ReadString('\n');
	}
}

func makelist(r *csv.Reader, matches *[][2]string) {
	line, err := r.Read();
	for ;err != io.EOF;{
			//fmt.Printf("%s\t%s\n", line[0], line[1]);
		*matches = append(*matches, [2]string{line[0], line[1]});
		line, err = r.Read();
	}
	
}

func comp(p1 []string, p2 [2]string) int{
	v1 := strings.Compare(p1[0], p2[0]);
	if v1 == 0 {
		return strings.Compare(p1[1], p2[1]);
	}
	return v1;
}

func findmatches(r *csv.Reader, matches *[][2]string, r_out *csv.Writer){
	line, err := r.Read();
	for ;err != io.EOF;{
		
		
		i := sort.Search(len(*matches), func(i int) bool {
				return comp(line, (*matches)[i]) <= 0;
				});
		if i < len(*matches) && comp(line, (*matches)[i]) == 0 {
			r_out.Write(line);
			fmt.Printf("%s\t%s\n", line[0], line[1]);
		} else {
			// x is not present in data,
			// but i is the index where it would be inserted.
		}
		
		line, err = r.Read();
	}
}

func main() {
	
	if len(os.Args) != 4 {
		fmt.Printf("programname ast lines_to_match output\n");
		os.Exit(1);
	}
	
	file_name_ast := os.Args[1];
	file_name_prefixes := os.Args[2];
	file_name_out := os.Args[3];
	
	f_ast, err := os.Open(file_name_ast);
	if err != nil {
	    log.Fatal(err)
	}
	f_prefixes, err2 := os.Open(file_name_prefixes);
	if err2 != nil {
	    log.Fatal(err2)
	}
	f_out, err3 := os.Create(file_name_out);
	if err3 != nil {
	    log.Fatal(err3)
	}
	r_out := csv.NewWriter(bufio.NewWriter(f_out));	
	
	
	r_ast := bufio.NewReader(f_ast)

	pr, pw := io.Pipe();
	
	pw2 := csv.NewWriter(pw);
	
	//go func() {
	//    defer pw.Close();
	//}()
	_=pw2;
	_=r_out;
	
	
	
	
	matches := [][2]string{};
	makelist(csv.NewReader(bufio.NewReader(f_prefixes)), &matches);
	
	go func(){
	}()
	
	go func(){
		defer pw.Close();
		extract(r_ast, pw2, "", "");
		pw2.Flush();
	}()
	
	findmatches(csv.NewReader(pr), &matches, r_out);	
	
	_ = pr;
	_ = pw;
	_ = r_ast;
	_ = file_name_prefixes;
	_ = file_name_out;
	_ = matches;
	
	r_out.Flush();
	f_out.Close();
}


