// 05 Nov 2020, Panmux

const fs = require("fs");
const path = require("path");
const titleMap = require("./fileTitle");
const latinize = require('latinize')
let pathArray = [];

function ThroughDirectory(Directory) {
  // https://stackoverflow.com/a/63111390
  fs.readdirSync(Directory).forEach((File) => {
    const Absolute = path.join(Directory, File);
    if (fs.statSync(Absolute).isDirectory()) return ThroughDirectory(Absolute);
    else return pathArray.push(Absolute);
  });
}

function copyWithFileName(inDIr, outDIr, toScript = "ro") {
  ThroughDirectory(inDIr);
  fs.mkdirSync(outDIr, { recursive: true });
  let i = 0;
  let lenP = pathArray.length;
  console.log("Total files: " + lenP);
  for (let f of pathArray) {
    let r = f.split("/");
    let filename = r[r.length - 1].replace(".txt", "");
    let fc = fs.readFileSync(f, { encoding: "utf-8", flag: "r" });
    // let endScript = tipitakaApp.TextProcessor.basicConvert(fc, toScript);
    let newFilePath = f
      .replace(inDIr, outDIr)
      .replace(".txt", "_" + latinize(titleMap[filename]) + ".txt");
    fs.writeFileSync(newFilePath, fc);
    i++;
    console.log(i + ". Converted: " + f);
  }
  console.log("");
  console.log("Done! Processed: " + i + "/" + lenP + " files");
}

copyWithFileName("text-plain-ro", "text-plain-ro-title");
