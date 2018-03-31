const { Client } = require('ynlu');
const { ClassifierHandler } = require('bottender');
// const B = require('bottender-compose');
const { spawn } = require('child_process');
var child1 = spawn('python3', ['../fatigue-master/chatdata.py']);
var c2 = spawn('cat', ['../fatigue-master/chatdata.txt'])
var txt = ''
c2.stdout.on('data', (data) => {
  txt = `${data}`;
});


const YNLU_TOKEN =
  process.env.YNLU_TOKEN ||
  'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjIwLCJleHBpcmVkQXQiOiIyMDE4LTA0LTAyVDAwOjAwOjAwLjAwMFoiLCJpYXQiOjE1MjIyMDY0NTl9.FfAB3qRCFJcOu9yfNMLon6mW2ITiPg3VtwiGZFP41pk';

const client = Client.connect(YNLU_TOKEN);
const classifier = client.findClassifierById('154025346121864532'); 
const tired_strings = [ '護眼體操舒緩疲勞 https://health.udn.com/health/story/5970/367431',
                        '媽媽叫你回家睡覺',
                        '幫你跟老闆請假了，回家睡吧，這個月薪水也跟家裡要',
                      ]
const chat_strings =  [ 'OAO',
                        'XD',
                        '哈哈好喔',
                        '＠＠',
                        '喔喔'                                                
                      ]
const music_strings = [ '聽三小音樂啦幹',
                        '去youtube啊 https://www.youtube.com',
                        '可是我不想幫你放音樂ㄟ'
                      ]
const salary_strings =[ '幫你寄信給老闆',
                        '我們要共體時艱',
                        '想當年我做多辛苦都沒抱怨薪水',
                        '草莓族還整天想加薪',
                        '有問題自己去跟老闆講，chatbot不能公親變事主啊'
                      ]
const ace_strings =   [ '有問題請聯絡學術部最大尾王秉倫',
                        '學術部的問題找王秉倫就對啦',
                        '去學術部找王秉倫'
                      ]
const info_strings =  [ '有問題請聯絡資訊部最大尾王秉倫',
                        '資訊部的問題找王秉倫就對啦',
                        '去資訊部找王秉倫'
                      ]
const public_strings =[ '有問題請聯絡電機當家男公關王秉倫',
                        '公關問題找王秉倫就對啦',
                        '你可以去公關部指名男公關王秉倫'
                      ]
const unknown_strings =[ '不會用chatbot請找王秉倫',
                        '聽譕啦',
                        '不要玩弄我QQ',
                        '你是要找王秉倫嗎',
                        '我不懂你講什麼',
                        '聽不懂'
                      ]



module.exports = new ClassifierHandler(classifier, 0.5)
  .onIntent('疲勞', async (context, result) => {
    child1 = spawn('python3', ['../fatigue-master/chatdata.py']);
    c2 = spawn('cat', ['../fatigue-master/chatdata.txt'])
    c2.stdout.on('data', (data) => {
      txt = `${data}`;
    });    
    await context.sendText(
      txt
      //tired_strings[Math.floor(Math.random() * Math.floor(3))]
    );
  })
  .onIntent('閒聊', async (context, result) => {
    child1 = spawn('python3', ['../fatigue-master/chatdata.py']);
    c2 = spawn('cat', ['../fatigue-master/chatdata.txt'])
    c2.stdout.on('data', (data) => {
      txt = `${data}`;
    });  
    await context.sendText(
      chat_strings[Math.floor(Math.random() * Math.floor(5))]      
    );
  })
  .onIntent('影音播放', async (context, result) => {
    child1 = spawn('python3', ['../fatigue-master/chatdata.py']);
    c2 = spawn('cat', ['../fatigue-master/chatdata.txt'])
    c2.stdout.on('data', (data) => {
      txt = `${data}`;
    });  
    await context.sendText(
      music_strings[Math.floor(Math.random() * Math.floor(3))]
    );
  })
  .onIntent('加薪', async (context, result) => {
    child1 = spawn('python3', ['../fatigue-master/chatdata.py']);
    c2 = spawn('cat', ['../fatigue-master/chatdata.txt'])
    c2.stdout.on('data', (data) => {
      txt = `${data}`;
    });  
    await context.sendText(
      salary_strings[Math.floor(Math.random() * Math.floor(5))]
    );
  })
  .onIntent('學術部', async (context, result) => {
    child1 = spawn('python3', ['../fatigue-master/chatdata.py']);
    c2 = spawn('cat', ['../fatigue-master/chatdata.txt'])
    c2.stdout.on('data', (data) => {
      txt = `${data}`;
    });  
    await context.sendText(
      ace_strings[Math.floor(Math.random() * Math.floor(3))]
    );
  })
  .onIntent('資訊部', async (context, result) => {
    child1 = spawn('python3', ['../fatigue-master/chatdata.py']);
    c2 = spawn('cat', ['../fatigue-master/chatdata.txt'])
    c2.stdout.on('data', (data) => {
      txt = `${data}`;
    });  
    await context.sendText(
      info_strings[Math.floor(Math.random() * Math.floor(3))]
    );
  })
  .onIntent('公關部', async (context, result) => {
    child1 = spawn('python3', ['../fatigue-master/chatdata.py']);
    c2 = spawn('cat', ['../fatigue-master/chatdata.txt'])
    c2.stdout.on('data', (data) => {
      txt = `${data}`;
    });  
    await context.sendText(
      public_strings[Math.floor(Math.random() * Math.floor(3))]      
    );
  })
  .onUnmatched(async (context, result) => {
    child1 = spawn('python3', ['../fatigue-master/chatdata.py']);
    c2 = spawn('cat', ['../fatigue-master/chatdata.txt'])
    c2.stdout.on('data', (data) => {
      txt = `${data}`;
    });  
    await context.sendText(
      unknown_strings[Math.floor(Math.random() * Math.floor(6))]      
    );
  });
