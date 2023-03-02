//Google Apps Script. Need to be pasted on the code.gs file

function doGet() {
  var html = HtmlService.createHtmlOutputFromFile('index');
  return html.setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}


function uploadFiles(data)
{
 var file = data.myFile;
 var folder = DriveApp.getFolderById('1lBiQI_3BxF2IcnMvoTDC7pAur6brKrtB');
 var createFile = folder.createFile(file);
 return createFile.getUrl();
}



client id : 846991818923-s1j9e6ka8tel0in38mn9oi65uo7fnvqi.apps.googleusercontent.com
client secret : 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