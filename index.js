const { ConsoleBot } = require('bottender');
const nluHandler = require('./nlu');
//const B = require('bottender-compose');

const bot = new ConsoleBot();

bot.onEvent(nluHandler);

bot.createRuntime();
