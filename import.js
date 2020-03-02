const mongodb = require('mongodb')
const path = require('path')
const fs = require('fs')
const dateFormat = require('dateformat')

async function process_file(dirPath, file, collection) {
	console.log(file)
	data = fs.readFileSync(path.join(dirPath, file), 'utf8').split('\n')
	for (let i = 0; i < data.length; i++) {
		if (!(data[i].includes('***') || data[i].includes('CONFIG'))) {
			tmp_data = data[i].split(',')
			date = tmp_data[0].split('/')
			date = [date[2], date[0], date[1]]
			let jsonData = {
				'Time': new Date(Date.parse(date.join('-') + 'T' + tmp_data[1])),
				'Power': Number(tmp_data[2])
			}
			console.log(jsonData)
			collection.updateOne({"Time": jsonData['Time']}, {"$set": jsonData}, {"upsert": true})
		}
	}
}

async function main() {
	var mongoClient = mongodb.MongoClient
	var url = "mongodb://sv2.teambit.tech/"
	var srv = await mongoClient.connect(url)
	var db = srv.db('weather')
	var collection = db.collection('rxpower')

	let dir = 'rxpower'
	const dirPath = path.join(__dirname, dir)
	fs.readdir(dirPath, (err, files) => {
		if (err) {
			console.log(err)
		} else {
			files.forEach(async (file) => {
				await process_file(dirPath, file, collection)
			})
		}
	})
}

main(() => {
	console.log("Hello")
})