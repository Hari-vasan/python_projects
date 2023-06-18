const { Client, LocalAuth } = require('./index');
const fs = require('fs');
const mysql = require('mysql');



const connection = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password: 'admin',
    database: 'whatsup_mebers'
});


const client = new Client({
    authStrategy: new LocalAuth(),
    // proxyAuthentication: { username: 'username', password: 'password' },
    puppeteer: { 
        // args: ['--proxy-server=proxy-server-that-requires-authentication.example.com'],
        headless: false
    }
});

client.initialize();

client.on('loading_screen', (percent, message) => {
    console.log('LOADING SCREEN', percent, message);
});

client.on('qr', (qr) => {
    console.log('QR RECEIVED', qr);
});

client.on('authenticated', () => {
    console.log('AUTHENTICATED');
});

client.on('auth_failure', msg => {
    console.error('AUTHENTICATION FAILURE', msg);
});

client.on('ready', async () => {

    console.log('READY');

    const chats = await client.getChats();

    const groups = chats.filter(c => c.isGroup);

    const names = groups.map(g => g.name)
    const puppeteerPage = client.pupPage; 
            const xpath = `(//p[@class='selectable-text copyable-text iq0m558w'])[1]`;
            await puppeteerPage.waitForTimeout(5000); 
            for (const name of names) {
                const elements = await puppeteerPage.$x(xpath);
                if (elements.length > 0) {
                    await elements[0].click();
                    await elements[0].type(name);
                    await puppeteerPage.waitForTimeout(3000);
                    const group_name_xpath = `(//span[@class='matched-text _11JPr'])[1]`;
                    const group_name = await puppeteerPage.$x(group_name_xpath);
                    await group_name[0].click();
                    await puppeteerPage.waitForTimeout(5000);
                    const group_members_xpath = `(//div[@class='p357zi0d r15c9g6i g4oj0cdv ovllcyds l0vqccxk pm5hny62'])[1]`
                    const group_members = await puppeteerPage.$x(group_members_xpath);
                    if (group_members.length > 0) {
                        for (const member of group_members) {
                            const textContent = await puppeteerPage.evaluate(element => element.textContent, member);
                            const name_convert=name.replace(/[^\w\s]/g, '');
                            const membersArray = textContent.split(',');
                            for (const member of membersArray) {
                                const trimmedMember = member.trim(); 
                                const finalMember = trimmedMember.replace(/\b(you)\b/gi, '');
                                if (finalMember !== ''){
                                    const sql = 'INSERT INTO members_data (group_name, phone_number) VALUES (?, ?)';
                                    const values = [name_convert, finalMember];
                                    connection.query(sql, values);
                                }
                             
                            }
                        }} else {
                        console.error('Element not found with XPath:', group_members_xpath);
                    }
                    const exit_button_xpath=`//div[@id='side']/div/div/div/button/div[2]/span`
                    const exit_button = await puppeteerPage.$x(exit_button_xpath);
                    await  exit_button[0].click()
                    await puppeteerPage.waitForTimeout(2000); 
                } else {
                    console.error('Element not found with XPath:', xpath);
                }
            }
            connection.end((err) => {
                if (err) {
                    console.error('Error closing MySQL connection:', err);
                }
                console.log('MySQL connection closed successfully.');
            });
            client.destroy();
        }
);