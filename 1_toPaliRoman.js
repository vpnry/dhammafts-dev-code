// Convert sinh text to Romanised Pali Text
// 05 Nov 2020, Panmux

const fs = require("fs");
const tipitakaApp = require("./0_pali-script.js");
const path = require("path");
let pathArray = [];

function ThroughDirectory(Directory) {
  // https://stackoverflow.com/a/63111390
  fs.readdirSync(Directory).forEach((File) => {
    const Absolute = path.join(Directory, File);
    if (fs.statSync(Absolute).isDirectory()) return ThroughDirectory(Absolute);
    else return pathArray.push(Absolute);
  });
}

function toPaliUtf8(inDIr, outDIr, toScript = "ro") {
  ThroughDirectory(inDIr);
  fs.mkdirSync(outDIr, { recursive: true });
  let i = 0;
  let lenP = pathArray.length;
  console.log("Total files: " + lenP);
  for (let f of pathArray) {
    let fc = fs.readFileSync(f, { encoding: "utf-8", flag: "r" });
    let endScript = tipitakaApp.TextProcessor.basicConvert(fc, toScript);
    let newFilePath = f.replace(inDIr, outDIr);
    fs.writeFileSync(newFilePath, endScript);
    i++;
    console.log(i + ". Converted: " + f);
  }
  console.log("");
  console.log("Done! Processed: " + i + "/" + lenP + " files");
}

toPaliUtf8("text-plain", "text-plain-ro", "ro");
