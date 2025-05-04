const { Client, GatewayIntentBits, Collection } = require('discord.js');
const { token } = require('./config.json');
const fs = require('fs');
const path = require('path');

const client = new Client({ intents: [GatewayIntentBits.Guilds, GatewayIntentBits.MessageContent] });

// Load all commands dynamically
client.commands = new Collection();
const commandFiles = fs.readdirSync('./commands').filter(file => file.endsWith('.js'));

for (const file of commandFiles) {
  const command = require(`./commands/${file}`);
  client.commands.set(command.data.name, command);
}

// Event when the bot is ready
client.once('ready', () => {
  console.log(`${client.user.tag} is online and ready!`);

  // Register commands globally if necessary
  // client.application.commands.set(client.commands.map(command => command.data)); // Optional for global commands
});

// Command to add an event
client.on('messageCreate', async (message) => {
  if (message.author.bot) return;

  const prefix = '!';
  if (!message.content.startsWith(prefix)) return;

  const args = message.content.slice(prefix.length).split(/ +/);
  const commandName = args.shift().toLowerCase();

  if (commandName === 'addevent') {
    const eventName = args[0];
    const eventDate = args[1];
    const eventDescription = args.slice(2).join(' ');

    // Save event to a JSON file or perform necessary actions
    const eventData = {
      event_name: eventName,
      event_date: eventDate,
      event_description: eventDescription
    };

    fs.readFile('events.json', 'utf8', (err, data) => {
      let events = [];
      if (!err && data) {
        events = JSON.parse(data);
      }

      events.push(eventData);

      fs.writeFile('events.json', JSON.stringify(events, null, 2), (err) => {
        if (err) {
          message.reply('There was an error saving the event.');
        } else {
          message.reply(`Event "${eventName}" added successfully!`);
        }
      });
    });
  }

  // Command to show events
  if (commandName === 'events') {
    fs.readFile('events.json', 'utf8', (err, data) => {
      if (err || !data) {
        return message.reply('No events found.');
      }

      const events = JSON.parse(data);
      if (events.length === 0) {
        return message.reply('No events found.');
      }

      let eventList = 'List of events:\n';
      events.forEach(event => {
        eventList += `**${event.event_name}** - ${event.event_date}: ${event.event_description}\n`;
      });
      message.reply(eventList);
    });
  }

  // Command to delete an event
  if (commandName === 'deleteevent') {
    const eventName = args.join(' ');

    fs.readFile('events.json', 'utf8', (err, data) => {
      if (err || !data) {
        return message.reply('No events found.');
      }

      let events = JSON.parse(data);
      events = events.filter(event => event.event_name !== eventName);

      fs.writeFile('events.json', JSON.stringify(events, null, 2), (err) => {
        if (err) {
          message.reply('There was an error deleting the event.');
        } else {
          message.reply(`Event "${eventName}" deleted successfully.`);
        }
      });
    });
  }
});

// Command to change language (example)
client.on('messageCreate', async (message) => {
  if (message.content.startsWith('!setlanguage')) {
    const langCode = message.content.split(' ')[1];

    // Assuming you have language files in 'languages' folder (e.g., en.json, es.json)
    const langFilePath = path.join(__dirname, 'languages', `${langCode}.json`);
    fs.readFile(langFilePath, 'utf8', (err, data) => {
      if (err) {
        return message.reply('Language not supported or error loading language.');
      }

      const language = JSON.parse(data);
      // Now, you can use 'language' object in your responses
      message.reply(`Language changed to ${langCode}.`);
    });
  }
});

// Log in to Discord with the app's token
client.login(token);
