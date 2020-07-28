import os
from flask import Flask, render_template, redirect, request, url_for, flash
from flask_paginate import Pagination, get_page_args
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

if os.path.exists('env.py'):
    import env


app = Flask(__name__)
app.config["MONGO_DBNAME"] = os.environ.get('MONGO_DBNAME')
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')


mongo = PyMongo(app)


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html', selected_home="selected")


@app.route('/enemy-list')
def enemy_index():

    query = []
    query_item = {}
    has_filter = False
    search = ''
    attack = ''
    level = ''

    def get_records(offset=0, per_page=10):
        return result[offset: offset + per_page]

    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')

    if 'search' in request.args:
        search = request.args.get('search').lower()
        query_item["name"] = { "$regex": search, "$options": "i" }
        query.append(query_item)
        has_filter = True

    if 'attack-type' in request.args:
        attack = request.args.get('attack-type')
        query_item["attack_type"] = attack
        query.append(query_item)
        has_filter = True

    if 'level-type' in request.args:
        level = request.args.get('level-type')
        query_item["level"] = level
        query.append(query_item)
        has_filter = True

    if has_filter == True:
        if len(query) > 0:
            result = mongo.db.enemyIndexMDB.find({"$and": query})
            paginate_results = get_records(offset=offset, per_page=per_page)
            pagination = Pagination(page=page, per_page=per_page, total=result.count())
            return render_template('enemyIndex.html', selected_enemy="selected", enemyIndexMDB=result, pagination=pagination, page=page, per_page=per_page, attack=attack, level=level)
        else:
            flash('No search results or no filters selected.')
            return redirect(url_for('enemy_index'))
    else:
        result = mongo.db.enemyIndexMDB.find()
        paginate_results = get_records(offset=offset, per_page=per_page)
        pagination = Pagination(page=page, per_page=per_page, total=result.count())
        return render_template('enemyIndex.html', selected_enemy="selected", enemyIndexMDB=result, pagination=pagination, page=page, per_page=per_page)

# @app.route('/enemy-list')
# def enemy_index():
#     if 'search' in request.args:
#         search = request.args.get('search')

#         if search == '':
#             flash('A keyword is required!')
#             return redirect(url_for('enemy_index'))


#         search = search.lower()
#         result = mongo.db.enemyIndexMDB.find({'name': { "$regex": search, "$options": "i" }})

#         if result.count() > 0:
#             return render_template('enemyIndex.html', enemyIndexMDB=result)
#         else:
#             flash('No results found.')
#             return redirect(url_for('enemy_index'))

#     else:
#         enemyIndexMDB = mongo.db.enemyIndexMDB.find()
#         return render_template('enemyIndex.html', enemyIndexMDB=enemyIndexMDB)


# @app.route('/enemy-list', methods=['GET', 'POST'])
# def filter_enemyIndex():

#     query = []
#     query_item = {}
#     queryValue = {}

#     if 'attack-type' in request.form:
#         items = request.form.get('attack-type')
#         query_item["attack_type"] = items
#         query.append(query_item)

#     if 'level-type' in request.form:
#         queryLevel = request.form.get('level-type')
#         query_item["level"] = queryLevel
#         query.append(query_item)

#     if len(query) > 0:
#         result = mongo.db.enemyIndexMDB.find({"$and": query})
#         return render_template('enemyIndex.html', enemyIndexMDB=result)
#     else:
#         flash('No filters selected.')
#         return redirect(url_for('enemy_index'))


@app.route('/enemy-list/<enemy_code>')
def more_info_enemy(enemy_code):
    the_enemy = mongo.db.enemyIndexMDB.find({'_id': ObjectId(enemy_code)})
    return render_template('moreInfoEnemy.html', enemy=the_enemy)


@app.route('/stage-list')
def stage_index():

    query = []
    query_item = {}
    has_filter = False
    search = ''
    episode = ''

    def get_records(offset=0, per_page=10):
        return result[offset: offset + per_page]

    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')

    if 'search' in request.args:
        search = request.args.get('search').lower()
        query_item["name"] = { "$regex": search, "$options": "i" }
        query.append(query_item)
        has_filter = True
    
    if 'episodes' in request.args:
        episode = request.args.get('episodes')
        query_item["episode_name"] = episode
        query.append(query_item)
        has_filter = True

    if has_filter == True:
        if len(query) > 0:
            result = mongo.db.stageIndexMDB.find({"$and": query})
            paginate_results = get_records(offset=offset, per_page=per_page)
            pagination = Pagination(page=page, per_page=per_page, total=result.count())
            return render_template('stageIndex.html', selected_stage="selected", stages=result, pagination=pagination, page=page, per_page=per_page, episode=episode)
        else:
            flash('No search results or no filters selected.')
            return redirect(url_for('stage_index'))
    else:
        result = mongo.db.stageIndexMDB.find()
        paginate_results = get_records(offset=offset, per_page=per_page)
        pagination = Pagination(page=page, per_page=per_page, total=result.count())
        return render_template('stageIndex.html', selected_stage="selected", stages=result, pagination=pagination, page=page, per_page=per_page)

    result = mongo.db.stageIndexMDB.find()
    return render_template('stageIndex.html', selected_stage="selected", stages=result)


@app.route('/stage-list/<stage_code>')
def more_info_stage(stage_code):
    the_stage = mongo.db.stageIndexMDB.find_one({'_id': ObjectId(stage_code)})

    enemies = []
    for enemy_id in the_stage["enemy_list"]:
        enemy = mongo.db.enemyIndexMDB.find_one({'_id': ObjectId(enemy_id)})
        enemies.append(enemy)
    
    return render_template('moreInfoStage.html', stage=the_stage, enemy=enemies)


@app.route('/statistics')
def statistics():
    query = []
    query_item = {}
    has_filter = False
    episode_statistics = ''

    pie_colors = [
        '#F7464A', '#46BFBD', '#FDB45C', 
        '#FEDCBA', '#ABCDEF', '#DDDDDD', '#ABCABC'
    ]

    if 'episode_statistics' in request.args:
        episode_statistics = request.args.get('episode_statistics')
        query_item["episode_name"] = episode_statistics 
        query.append(query_item)
        episode_result = mongo.db.stageIndexMDB.find({"$and": query})

        enemies = []
        for stage in episode_result:
            for enemy in stage['enemy_list']:
                if enemy not in enemies:
                    enemies.append(enemy)
        
        if len(enemies) > 0:
            has_filter = True
        
    results_attack_type = []
    results_level_type = []

    if has_filter == True:
        results_attack = mongo.db.enemyIndexMDB.aggregate([
            { 
                "$match": { '_id' : { "$in" : enemies } }
            },
            {
                "$group": {
                    "_id": "$attack_type",
                    "count": { "$sum": 1 } 
                }
            }
        ])

        results_level = mongo.db.enemyIndexMDB.aggregate([
            { 
                "$match": { '_id' : { "$in" : enemies } }
            },
            { 
                "$group": {
                    "_id": "$level",
                    "count": { "$sum": 1 } 
                }
            }
        ])
        
    else:
        results_attack = mongo.db.enemyIndexMDB.aggregate([
            { "$group": {
                "_id": "$attack_type",
                "count": { "$sum": 1 } 
            }}
        ])

        results_level = mongo.db.enemyIndexMDB.aggregate([
            { "$group": {
                "_id": "$level",
                "count": { "$sum": 1 } 
            }}
        ])

    results_attack_type = []
    pie_attack_type_labels = []
    
    results_level_type = []
    pie_level_type_labels = []

    for item in results_attack:
        results_attack_type.append(item["count"])
        pie_attack_type_labels.append(item["_id"].title())

    for item in results_level:
        results_level_type.append(item["count"])
        pie_level_type_labels.append(item["_id"].upper())
    
    return render_template('statistics.html', episode_statistics=episode_statistics, selected_statistics="selected", pie_attack_type_values=results_attack_type, pie_attack_type_labels=pie_attack_type_labels, pie_colors=pie_colors, pie_level_type_values=results_level_type, pie_level_type_labels=pie_level_type_labels)


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
