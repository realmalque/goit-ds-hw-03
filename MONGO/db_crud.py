from pymongo import MongoClient

# Вказуємо ваш MongoDB URI
client = MongoClient("mongodb+srv://realmalque:amlque123321@cluster0.fofyqea.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

# Підключення до бази даних
db = client["mydatabase"]

# Підключення до колекції
collection = db["cats"]


def read_all():
    documents = collection.find()
    for document in documents:
        print(document)

def read_cat_by_name(name):
    print (collection.find_one({"name": name}))

def update_age_by_name (name, new_age):
    return collection.update_one({"name": name}, {"$set": {"age": new_age}})

def new_feature_by_name (name, new_feature):
    return collection.update_one({"name": name},{"$addToSet": {"features": new_feature}})

def del_by_name(name):
    return collection.delete_one({"name": name})

def drop_all():
    return collection.delete_many({})

if __name__ == "__main__":
    # print(read_all())
    # print(update_age_by_name('vaska','12'))
    # print(read_cat_by_name('vaska'))
    # print(new_feature_by_name('vaska', 'сильно ліняє'))
    # print(del_by_name("simba"))
    print(drop_all())