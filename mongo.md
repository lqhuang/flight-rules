---
title: MongoDB Tips
---

## Query last record or fisrt record

```javascript
db.collection
  .find()
  .sort(($natural: -1))
  .limit(1);
```

## Mongoegine

### mongoegine Model class 可以默认指定 collection

> Document classes that inherit **directly** from `Document` will have their own **collection** in the database. The name of the collection is by default the name of the class, converted to lowercase (so in the example above, the collection would be called page). If you need to change the name of the collection (e.g. to use MongoEngine with an existing database), then create a class dictionary attribute called `meta` on your document, and set `collection` to the name of the collection that you want your document class to use:

rule: UserInfo -> user_info

If you want to specify it:

```python
class Page(Document):
    title = StringField(max_length=200, required=True)
    meta = {'collection': 'cmsPage'}
```

references:

(1) [specifying-collection-name-with-mongoengine](https://stackoverflow.com/questions/53976963)specifying-collection-name-with-mongoengine
(2) [document-collections](http://docs.mongoengine.org/guide/defining-documents.html#document-collections)
(3) [mongoengine 中 collection 名称自动生成机制浅探 - Chinese](https://www.cnblogs.com/AcAc-t/p/mongoengine_collection_name.html)

### to dictionary

way 1:

calling .to_mongo() converts the object to a SON instance. Once you have it, you can call its .to_dict() method to convert it to a dictionary.

```python
sons = [ob.to_mongo() for ob in query_set]
for son in sons:
    d = son.to_dict()
```

way 2: just return raw values from pymongo

    Page.objects().as_pymongo()

references:

(1) [convert-mongodb-return-object-to-dictionary](https://stackoverflow.com/questions/13230284/convert-mongodb-return-object-to-dictionary)
(2) [mongoengine.queryset.QuerySet.as_pymongo](http://docs.mongoengine.org/apireference.html#mongoengine.queryset.QuerySet.as_pymongo)

### exclude "\_id"

```python
# there is one exception for _id field,
# which will be excluded even if only() is called,
# actually the following is the only way to exclude _id field
BlogPost.objects.only('title').exclude('_id').find_all(..
```

References:

1. https://motorengine.readthedocs.io/en/latest/getting-and-querying.html#motorengine.queryset.QuerySet.exclude
2. https://github.com/MongoEngine/mongoengine/issues/641

# 删除 sentiment.prediction 一定范围内的数据

```javascript
db.getCollection("prediction").deleteMany({
  timestamp_ms: {
    $gte: "1573948800000",  # 2019-11-17 00:00:00+00:00
    $lt: "1574089200000", # 2019-11-18 15:00:00+00:00
  }
})
```

```javascript
db.getCollection("prediction").deleteMany({
  timestamp_ms: {
    $gte: "1573948800000",  # 2019-11-17 00:00:00+00:00
    $lt: "1574089200000", # 2019-11-18 15:00:00+00:00
  }
})
```

## Aggregation operations

Refs:

1. [Aggregation Pipeline Stages](https://docs.mongodb.com/manual/reference/operator/aggregation-pipeline)

## Count number of distinct values for target field/key

```javascript
db.articles.aggregate(
  [
    {
      $match: {
        keywords: { $not: { $size: 0 } },
      },
    },
    {
      $group: {
        _id: "$keywords",
        count: { $sum: 1 },
      },
    },
    { $sort: { count: -1 } },
    { $limit: 100 },
  ],
  { allowDiskUse: true }
);
```

Refs

1. [mongodb count num of distinct values per field/key](https://stackoverflow.com/questions/14924495/mongodb-count-num-of-distinct-values-per-field-key)

## Remove duplicates in same collection

```javascript
var duplicates = [];

db.getCollection("coll")
  .aggregate(
    [
      {
        $group: {
          _id: { tweet_id: "$tweet_id" },
          dups: { $addToSet: "$_id" },
          count: { $sum: 1 },
        },
      },
      {
        $match: {
          count: { $gt: 1 },
        },
      },
    ],
    { allowDiskUse: true }
  )
  .forEach(function (doc) {
    doc.dups.shift();
    doc.dups.forEach(function (dupId) {
      duplicates.push(dupId);
    });
  });
// printjson(duplicates);

// Remove all duplicates in one go
db.getCollection("coll").remove({
  _id: { $in: duplicates },
});
```

Now we will do an analysis of the above-written query.
1. `var duplicatesIds = []`: This is an array declaration where this query will push the duplicate IDs.

2. `{$group:{_id:{EmpId:"$EmpId"},dups:{"$addToSet":"$_id"} ,count:{"$sum":1}}}`: Here we are grouping the records on behalf of `EmpId`, and using `$addToSet` command, we can create an array "dups", and `count:{"$sum":1}` is counting the duplicate records.

3. `{$match:{count:{"$gt":1}}}`: Here we are filtering the records that have a count greater than 1. As the above group pipeline, we are counting the duplicate records on behalf of `EmpId`.

4.  `ForEach`: we are iterating records one by one here which are grouped EmpId, here we will find the array of duplicate records, for example

```
"dups" : [
ObjectId("5e5f5d20cad2677f9f839327"),
ObjectId("5e5f5d27cad2677f9f839328"),
ObjectId("5e5f5cf8cad2677f9f839323")
]
```

5. `doc.dups.shift()`:Here we are removing one record which will not be deleted, and It means we will delete the duplicates except one document.

6. `doc.dups.forEach(function (dupId)`: here again, we are iterating the array to push (duplicatesIds.push(dupId)) it records (duplicatesIds)on the above-declared array.

7. `db.Employee.find()`: to fetch the records.
Now finally execute the above MongoDB query, and you will find the following records.

Refs:

1. [MongoDB Query: Remove duplicate records from collection except one](https://www.codefari.com/2020/03/mongodb-query-remove-duplicate-records.html)

## 针对已经存在的所有 documents 添加 serial number

```javascript
var i = 0;
db.myCollection.find({}, { _id: 1 }).forEach((doc) => {
  db.myCollection.update(
    { _id: doc._id },
    { $set: { serial_idx: NumberLong(i) } }
  );
  i += 1;
});
```

如果量太大的话,

```javascript
let myCursor = db.myCollection.find({}, { _id: 1 });
var i = 0;

while (myCursor.hasNext()) {
  let doc = myCursor.next();
  db.myCollection.update(
    { _id: doc._id },
    { $set: { serial_idx: NumberLong(i) } }
  );
  i += 1;
}
```

这个方法太慢了

```javascript
let myCursor = db.myCollection
  .find({}, { _id: 1 })
  .batchSize(500)
  .noCursorTimeout();

var i = 0;
var bulkUpdateOps = [];
var groupCount = 0;

while (myCursor.hasNext()) {
  let doc = myCursor.next();
  bulkUpdateOps.push({
    updateOne: {
      filter: { _id: doc._id },
      update: { $set: { serial_idx: NumberLong(i) } },
    },
  });

  i += 1;
  groupCount += 1;

  if (groupCount >= 10000) {
    db.myCollection.bulkWrite(bulkUpdateOps, { ordered: false });
    bulkUpdateOps = [];
    groupCount = 0;
  }
}
// Last group
db.myCollection.bulkWrite(bulkUpdateOps, { ordered: false });
```

Ref:

1. https://stackoverflow.com/questions/23839021/add-a-field-in-all-documents-in-an-existing-collection-mongodb
2. https://stackoverflow.com/questions/62326370/add-ascending-serial-number-field-to-all-existing-mongodb-documents-in-a-collect

## Experience `CursorNotFound` error

error info:

```
2020-11-19T21:25:37.570+0800 E QUERY    [js] [src/mongo/shell/utils.js:25:13] Error: getMore command failed: {
        "operationTime" : Timestamp(1605792329, 1),
        "ok" : 0,
        "errmsg" : "cursor id 1063168017591 not found",
        "code" : 43,
        "codeName" : "CursorNotFound",
        "$clusterTime" : {
                "clusterTime" : Timestamp(1605792329, 1),
                "signature" : {
                        "hash" : BinData(0,"5fLLDqv2LxDUvgUKjaq/ijiNzg4="),
                        "keyId" : NumberLong("6844415292555132929")
                }
        }
}
```

Solutions:

1. add `noCursorTimeout()` option;
2. reduce batch size by setting `batchSize(50)`;

Refs:

1. https://stackoverflow.com/questions/44248108/mongodb-error-getmore-command-failed-cursor-not-found/44250410
2. https://stackoverflow.com/questions/51526688/mongodb-cursornotfound-error-on-collection-find-for-a-few-hundred-small-record/51701154
