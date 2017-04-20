package main

import (
	"fmt"
	"log"
	"io"
	"os"
	"bufio"
	"golang.org/x/net/html"
	"strings"
	"strconv"
	"unicode"
	"unicode/utf8"
	"net/url"
	"encoding/json"
	"os/exec"
	"bytes"
	"golang.org/x/net/html/atom"
)

//1 - text
//2 - root doc
//3 - tags
//4 - comments <!-- -->

//	ErrorNode NodeType = iota
//	TextNode
//	DocumentNode
//	ElementNode
//	CommentNode
//	DoctypeNode

type Result struct{
    Rank         string
    URL         string
    Host         string
    Title       string
    Description string
    Body         string
    Language     string
    Links        []string
    Headers        map[string][]string
    LastModified []string
}
var count int;
var num_iframes int;//1
var num_hidden  int;//2
var num_small   int;//3
var num_script  int;//4
var has_meta    bool;//11
var num_embed   int;//12
var num_extern  int;//13
var num_url     int;//15
var has_dou     bool;//16

//html, head, title, body
var has_seen [4]bool;
var char_white int;
var char_total int;
var size_script int;
var curdomain  string;

func comp(p1 []string, p2 [2]string) int{
	v1 := strings.Compare(p1[0], p2[0]);
	if v1 == 0 {
		return strings.Compare(p1[1], p2[1]);
	}
	return v1;
}

//if
//while
//assign

/*type Statement = BlockStatement | BreakStatement | ContinueStatement |
DebuggerStatement | EmptyStatement |
ExpressionStatement  |
LabeledStatement | ReturnStatement | SwitchStatement |
ThrowStatement | TryStatement | VariableDeclaration |
 | WithStatement;
type Declaration = ClassDeclaration  VariableDeclaration*/

var hashmap map[string]int;

func makemap() {
	hashmap = make(map[string]int);
	
	hashmap["DoWhileStatement"] = 1;
	hashmap["IfStatement"] = 1;
	hashmap["ForStatement"] = 1;
	hashmap["ForInStatement"] = 1;
	hashmap["ForOfStatement"] = 1;
	hashmap["FunctionDeclaration"] = 1;
	hashmap["WhileStatement"] = 1;
}

func isContext (n string) bool {
	//fmt.Println(n);
	return hashmap[n] == 1;
}

var wholescript *string;

func parsescript2(r_ast *bufio.Reader, con string, featuremap *map[string]bool){
	
	
	cur := con;
	iscurcontext := false;
	line, err := r_ast.ReadString('\n');
	
		//for i:=0;i<10;i++ {
		//fmt.Printf(line);
	//line, err = r_ast.ReadString('\n');
		//}
		//return
	//var s, e int;
	for ;err != io.EOF; {
		_ = err;
		line = strings.Trim(line, " \t\r\n");
		if (strings.Contains(line,"{")){
			parsescript2(r_ast, cur, featuremap);
		} else if strings.Contains(line, "}") {
			return;
		} else if len(line) <= 2 {
		} else {
			
				//fmt.Println(line);
			pos := strings.Index(line,":");
			s1 := strings.Trim(line[0:pos], "\"");
			if strings.Compare(s1, "range") == 0 {
				var s, e int;
				line, err = r_ast.ReadString('\n');
				if err != nil {
					log.Fatal(err);
				}
				s, err = strconv.Atoi(strings.Trim(line," ,\t\r\n"));
				line, err = r_ast.ReadString('\n');
				if err != nil {
					log.Fatal(err);
				}
					//fmt.Printf("%s\n",line);
				e, err = strconv.Atoi(strings.Trim(line," ,\t\r\n"));
				r_ast.ReadString('\n');
				_=s;
				_=e;
					//fmt.Printf("%d\t%d\n", s, e);
				if !iscurcontext {
					//fmt.Printf("%s\t%s\n", con,(*wholescript)[s:e]);
					(*featuremap)[con + "," + (*wholescript)[s:e]] = true;
				}
			} else{
				s2 := strings.Trim(line[pos+1:], " ,\"");
				
					//fmt.Printf("%s\t%s\n", con, s2);
				if (strings.Compare(s1,"type") == 0){
					//fmt.Printf("%v\n", err2);
					//fmt.Printf("%s\t%s\n", con, s2);
					if isContext(s2) {
						//fmt.Println(hashmap[s2]);
						//fmt.Println(s2);
						cur = s2;
						iscurcontext = true;
					}
				}
			}
		}
		
		
		
		line, err = r_ast.ReadString('\n');
	}
	
	//fmt.Println(line);
	
	
	
	/*line, err := r.Read();
	for ;err != io.EOF;{
		
		
		i := sort.Search(len(*matches), func(i int) bool {
				return comp(line, (*matches)[i]) <= 0;
				});
		if i < len(*matches) && comp(line, (*matches)[i]) == 0 {
			//r_out.Write(line);
			fmt.Printf("%s\t%s\n", line[0], line[1]);
		} else {
			// x is not present in data,
			// but i is the index where it would be inserted.
		}
		
		line, err = r.Read();
	}*/
}

func parsescript(n string, featuremap *map[string]bool){
	
	cmd := exec.Command("node", "run.js");
	//f, err2 := os.Open("../alexa-detector/ast/test.js");
	//if err2 != nil {
	//	log.Fatal(err2);
	//}
	//tempstring := "function bubbleSort(list){var items=list.slice(0),swapped=!1,p,q;for(p=1;p<items.length;++p){for(q=0;q<items.length-p;++q)if(items[q+1]<items[q]){swapped=!0;let temp=items[q];items[q]=items[q+1],items[q+1]=temp;}if(!swapped)break;}return items;}";
	//wholescript = &tempstring;
	wholescript = &n;
	r := bufio.NewReader(strings.NewReader(n));
	
	
	
	cmd.Stdin = r;
	var out bytes.Buffer;
	cmd.Stdout = &out;
	err := cmd.Run()
	if err != nil {
		log.Println("Error with script: \t", n);
	}
	//r_ast := io.ByteReader(out);
	
	r_ast := bufio.NewReader(strings.NewReader(out.String()));
	_=r_ast;
	line, err := r_ast.ReadString('\n');
				if err != nil {
					log.Fatal(err);
				}
	_ = line;
	_ = err;
	parsescript2(r_ast, "", featuremap);
}


func parseline(s string) (int, int) {
	a := 0;
	b := len(s);
	for index, runeValue := range s {
		if unicode.IsSpace(runeValue) {
			a++;
		}
	_ = index;
    }
	return a, b;
}

func getDomain(s string) (string, bool) {
	s = strings.Trim(s, " \t\r\n\\\"'");
	//s = strings.Replace(s, "%%", "%", -1);
	//fmt.Println(s);
	
	pos := strings.Index(s, "\n");
	for ;pos>=0; pos=strings.Index(s, "\n") {
		s = s[0:pos] + s[pos+1:];
	}
	pos = strings.Index(s, " ");
	for ;pos>=0; pos=strings.Index(s, " ") {
		s = s[0:pos] + s[pos+1:];
	}
	
	u, err := url.Parse(s);
	if err != nil{
		//fmt.Println(s);
		//fmt.Println(err);
		return "",false;
	}
	
	return u.Host, true;
}

func traverse(n *html.Node, pref int, is_script_par bool, featuremap *map[string]bool) {
	//fmt.Println(n.Data);
	
	
	is_script := false;
	
	if n.Type == html.ErrorNode {
		
	} else if n.Type == html.TextNode {
		if is_script_par {
			size_script += len(n.Data);
		} else {
			a, b := parseline(n.Data);
			char_white += a;
			char_total += b;
		}
	} else if n.Type == html.DocumentNode {
		
	} else if n.Type == html.ElementNode {
		
		/*if n.DataAtom == atom.Script {
			for c := n.FirstChild; c != nil; c = c.NextSibling {
				parsescript(c.Data, featuremap);
			}
		}*/
		
		
		//1
		if n.DataAtom == atom.Iframe {
			num_iframes++;
		}
		//2
		for i:=0;i<len(n.Attr);i++ {
			if strings.Compare(n.Attr[i].Key, "hidden") == 0 {
				num_hidden++;
			}
		}
		//3
		if n.DataAtom == atom.Div || n.DataAtom == atom.Iframe || n.DataAtom == atom.Object {
			width, height := 100, 100;
			for i:=0;i<len(n.Attr);i++ {
				if strings.Compare(n.Attr[i].Key, "width") == 0 {
					w, err := strconv.Atoi(n.Attr[i].Val);
					if err == nil {
						width = w;
					}
				}
				if strings.Compare(n.Attr[i].Key, "height") == 0 {
					h, err := strconv.Atoi(n.Attr[i].Val);
					if err == nil {
						height = h;
					}
				}
				if strings.Compare(n.Attr[i].Key, "stlye") == 0 {
				}
			}
			if width*height<30 || width<2 || height<2 {
				num_small++;
			}
		}
		//4
		if n.DataAtom == atom.Script {
			num_script++;
		}
		//5
		//6
		if n.DataAtom == atom.Script {
			is_script = true;
			//fmt.Printf("%v\n", n.Attr);
		}
		//7
		//8
		//9
		//10
		//11
		if n.DataAtom == atom.Meta {
			for i:=0;i<len(n.Attr);i++ {
				if strings.Compare(n.Attr[i].Key, "http-equiv") == 0 {
					if strings.Compare(n.Attr[i].Val, "refresh") == 0 {
						has_meta = true;
					}
				}
			}
		}
		//12
		if n.DataAtom == atom.Embed || n.DataAtom == atom.Object {
			num_embed++;
		}
		//13
		for i:=0;i<len(n.Attr);i++ {
			if strings.Compare(n.Attr[i].Key, "src") == 0 {
				url := n.Attr[i].Val;
				sdomain, bdomain := getDomain(url);
				if bdomain {
					if strings.Compare(sdomain, curdomain) != 0 {
						num_extern++;
					}
				}
				if n.DataAtom == atom.Script || n.DataAtom == atom.Iframe ||
				   n.DataAtom == atom.Frame || n.DataAtom == atom.Embed ||  
				   n.DataAtom == atom.Form || n.DataAtom == atom.Object {
					num_url++;
				} 
			}
		}
		//14
		//15 - see 13
		//16
		//html.Parse() does not parse invalid title/body/etc tags
		/*if !has_dou {
			temp := [4]string{"html", "head", "title", "body"};
			for i:=0;i<4;i++ {
				if strings.Compare(n.Data, temp[i]) == 0 {
					fmt.Printf("%s\n", n.Data);
					if has_seen[i] {
						has_dou = true;
					} else {
						has_seen[i] = true;
					}
				}				
			}
		}*/
		//17
		//18
		
	} else if n.Type == html.CommentNode {
		
	} else if n.Type == html.DoctypeNode {
		
	}
	
	
	for c := n.FirstChild; c != nil; c = c.NextSibling {
		traverse(c, pref+1, is_script, featuremap);
	}
}

func create(r string, featuremap *map[string]bool){
	
	doc, err := html.Parse(strings.NewReader(r))
	if err != nil {
	    log.Fatal(err)
	}
	traverse(doc,-1, false, featuremap)
}

func main2(url string, r_in string, w_out *bufio.Writer) {
	/*if len(os.Args) != 3 {
		fmt.Printf("programname file_name address\n");
		os.Exit(1);
	}
	
	file_name := os.Args[1];*/
	var bdomain bool;
	num_iframes = 0;
	num_hidden  = 0;
	num_small   = 0;
	num_script  = 0;
	has_meta    = false;
	num_embed   = 0;
	num_extern  = 0;
	num_url     = 0;
	has_dou     = false;
	
	has_seen    = [4]bool{false, false, false, false};
	char_white  = 0;
	char_total  = 0;
	size_script = 0;
	curdomain, bdomain = getDomain(url);
	if !bdomain {
		return;
	}

	/*f, err := os.Open(file_name);
	if err != nil {
	    log.Fatal(err)
	}
	r := bufio.NewReader(f)*/
	//r := bufio.NewReader(strings.NewReader(r_in));
	
	file_size := len(r_in);
	
	var featuremap map[string]bool;
	featuremap = make(map[string]bool);
	create(r_in, &featuremap);
	for key, value := range featuremap {
		_=value;
		_=key;
	    //fmt.Println("Key:", key)
	}
	
	string_out := fmt.Sprintf("%d\n%d\n%d\n%d\n%f\n%f\n%v\n%d\n%d\n%d\n%d\n",
		num_iframes, num_hidden,
		num_small, num_script,
		float64(100*size_script)/float64(file_size), float64(100*char_white)/float64(char_total),
		has_meta, num_embed,
		num_extern, num_url,
		utf8.RuneCountInString(r_in));
	//buf_out := make([]byte, len(string_out));
	w_out.WriteString(string_out);
	
	//r := bufio.NewReader(f)*
	//r := bufio.NewReader(strings.NewReader(r_in));
	
	
	/*fmt.Printf("# Iframes: \t%d\n", num_iframes);//1
	fmt.Printf("# Hidden:  \t%d\n", num_hidden); //2
	fmt.Printf("# Small:   \t%d\n", num_small);  //3
	fmt.Printf("# Script:  \t%d\n", num_script); //4
	fmt.Printf("%% Script:  \t%f\n", float64(100*size_script)/float64(file_size)); //6
	fmt.Printf("%% White:   \t%f\n", float64(100*char_white)/float64(char_total));//10
	fmt.Printf("Has Meta:  \t%v\n", has_meta);   //11
	fmt.Printf("# Embeded: \t%d\n", num_embed);   //12
	fmt.Printf("# Extern:  \t%d\n", num_extern); //13
	fmt.Printf("# URLs:    \t%d\n", num_url);    //15
	fmt.Printf("# Char:    \t%d\n", utf8.RuneCountInString(r_in)); //18
	*/
	_=file_size;
	
}

func main(){
	makemap();
	count = 0;
	
	if len(os.Args) != 4 {
		fmt.Printf("programname mode db output\n");
		os.Exit(1);
	}
	
	//f, err := os.Open("sample_db.json");
	f, err := os.Open(os.Args[2]);
	if err != nil {
	    log.Fatal(err)
	}
	
	f_out, err_out := os.Create(os.Args[3]);
	if err_out != nil {
	    log.Fatal(err_out)
	}
	w_out := bufio.NewWriter(f_out);


	if os.Args[1][0] == '0' {//json db

		fi, err := f.Stat()
    	if err != nil {
            // Could not obtain stat, handle error
    	}
		var data []byte;
		data = make([]byte, fi.Size());
		r_db := bufio.NewReader(f);
		io.ReadFull(r_db, data);
	
		var results []Result
	
		err2 := json.Unmarshal(data, &results);
		if err2 != nil {
			fmt.Println("error:", err2)
		}
		
		/*shorter,err33 := json.Marshal(results[:400]);
		if err33 != nil {
			log.Fatal("Shorter");
		}
		_=shorter;
		w_out.Write(shorter);
		w_out.Flush();
		os.Exit(1);*/
		
		for i:=0;i<len(results);i++ {
			if count % 10 == 0 {
				fmt.Println(count);
			}
			count++;
			main2(results[i].URL, results[i].Body, w_out);
			//os.Exit(1);
		}
	} else if os.Args[1][0] == '1' {//dir
		names, err_dir := f.Readdirnames(-1);
		if err_dir != nil {
			log.Fatal(err_dir);
		}
		fmt.Println(len(names));
		for i:=0;i<len(names);i++ {
			//fmt.Println(names[i].Name());
			f_child, err_child := os.Open(os.Args[2]+names[i]);
			//fmt.Println(names[i]);
			if err_child != nil {
				log.Fatal(err_child);
				continue;
			}
			//fmt.Println(names[i]);
			fi, err_stat := f_child.Stat()
    		if err_stat != nil {
				continue;
    		}
			//fmt.Println(names[i]);
			var data []byte;
			data = make([]byte, fi.Size());
			io.ReadFull(bufio.NewReader(f_child), data);
			data_string := string(data);
			main2("", data_string, w_out);
		}
	} else {//Really? What is this?  Use an actual mode.
		fmt.Println("Invalid mode.\n");
		os.Exit(1);
	}
    
	
	
	
	
	
	
	
	w_out.Flush();
}

