// 05 Nov 2020, Panmux

const fs = require("fs");
let fc = fs.readFileSync("title.js.html", { encoding: "utf-8", flag: "r" });
// Use Visual Studio Code replace title.js.html with '<li file-id=' with '\n<li file-id=' first
fc = fc.split("\n");
let str = "";
let i = 0;
for (let line of fc) {
  line = line.trim();
  if (line.startsWith("<li file-id=")) {
    i++;
    str += line + "\n";
  }
}
fs.writeFileSync("onlywithID.txt", str);
console.log("Done: lines: " + i);
