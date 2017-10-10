import datetime
import hashlib
import hmac
import uuid

from flask import request, g, jsonify, session, url_for
from flask_login import login_required, current_user, login_user, logout_user
from pymongo.errors import DuplicateKeyError

from app import login_manager, mongo, log
from app.db.models import Admin
from app.tools import check
from app.tools import convert, encrypt
from app.views import api


ARTICLE_URL_TEMPLATE = 'http://whoyoung.me/article/{}'


@api.before_request
def before_request():
    g.user = current_user


@api.route('/logout')
def logout():
    logout_user()
    return jsonify({'status': 1})


@login_manager.user_loader
def load_user(oid):
    return Admin.find_by_oid(oid)


@api.route('/login_by_username', methods=['POST'])
def login():
    jsondata = request.json
    # POST. 取出 POST 请求参数
    username = jsondata['username']
    psw = jsondata['password']
    admin = Admin.find_by_username(username)
    hash_psw = hmac.new(session['salt'].encode(), admin.cryptPassword.encode(), hashlib.md5).hexdigest()
    # 密码相等
    if hash_psw == psw:
        login_user(admin, remember=True)
        # 后期不应该使用 salt 作为 tokena
        return jsonify({'status': 1})  # 登录成功
    else:
        logout_user()
        return jsonify({'status': 0})  # 登录失败


@api.route('/get_salt')
def get_salt():
    # 每次使用不一样的盐 salt
    salt = encrypt.create_salt()
    session['salt'] = salt
    log.info('salt: {}'.format(session['salt']))
    return jsonify({'salt': salt})


@api.route('/register', methods=['POST'])
def register():
    jsondata = request.json
    email = jsondata['email']
    psw = jsondata['password']   # password only deal with md5
    username = jsondata['username']
    intro = jsondata['intro']
    one_text = jsondata['oneText']
    intro_img_url = jsondata['introImgURL']
    social_account = jsondata['socialAccount']
    user_id = username       # 未来可以自定义 id，类似微信的自定义 id
    sign_up_time = datetime.datetime.utcnow()
    # 第一次插入
    try:
        # 先简答处理，后面需要对数据进行建模
        mongo.db.admins.insert({'email': email, 'cryptPassword': psw, 'username': username, 'intro': intro,
                                'oneText': one_text, 'introImgURL': intro_img_url, 'socialAccount': social_account,
                                'id': user_id, 'signUpTime': sign_up_time})
    except DuplicateKeyError:
        # 反馈失败原因
        # check.py username, email, id exist or not.
        result = mongo.db.admins.find_one({'email': email})
        if result:
            # 邮箱已经被注册
            return jsonify({'status': -1, 'msg': 'email:{} has been registered.'.format(email)})
        result = mongo.db.admins.find_one({'username': username})
        if result:
            # 用户名已经被注册
            return jsonify({'status': -2, 'msg': 'username:{} has been registered.'.format(username)})


@api.route('/post_article', methods=['POST'])
@login_required
def upload_post():
    """
    上传博客
    :return:
    """
    jsondata = request.json
    t = jsondata.get('tags', [])
    # tags 需要是一个 lists
    if not isinstance(t, list):
        return jsonify({'status': 0})
    tags = list()
    for item in t:
        # 因为跨域名问题，所以这里只能够手动拼 url
        tags.append({'name': item, 'id': item})
    uid = uuid.uuid4().hex
    post = {'title': jsondata['title'], 'tags': tags,
            'intro': jsondata.get('intro', ''), 'createdTime': datetime.datetime.utcnow(),
            'content': jsondata['content'], 'markdown': jsondata['markdown'],
            'author': {'username': g.user.username, 'email': g.user.email, 'id': g.user.username}, 'id': uid,
            'status': jsondata.get('status', 'published'), 'rate': 4,
            'browseNumber': 0, 'commentNumber': 0, 'likeNumber': 0}
    mongo.db.articles.insert_one(post)
    return jsonify({'status': 1, 'url': ARTICLE_URL_TEMPLATE.format(uid)})


@api.route('/upload/project', methods=['POST'])
@login_required
def upload_project():
    jsondata = request.json
    t = jsondata.get('tags', [])
    author = jsondata.get('author', [])
    if not isinstance(author, list):
        return '-1'
    if not isinstance(t, list):
        return '-1'
    tags = list()
    for item in t:
        # 因为跨域名问题，所以这里只能够手动拼 url
        tags.append({'name': item, 'url': '/tags/{}'.format(item)})
    uid = uuid.uuid4().hex
    author = jsondata['author']
    if not convert.is_author_format(author):
        return '-1'
    project = {'name': jsondata['name'], 'projectURL': jsondata['projectURL'], 'intro': jsondata['intro'],
               'author': author, 'tags': tags, 'browseNumber': 0, 'id': uid, 'isDel': False,
               'createdTime': datetime.datetime.utcnow()}
    mongo.db.projects.insert_one(project)
    return url_for('get_project', uid=uid)


@api.route('/upload/navinfo', methods=['POST'])
@login_required
def update_navinfo():
    jsondata = request.json
    if convert.is_navinfo_format(jsondata):
        mongo.db.navinfo.update({}, {'$set': jsondata}, True, False)
        return '1'
    else:
        return '-1'


@api.route('/get_article_by_id')
@login_required
def get_article_by_id():
    uid = request.args['id']
    article = mongo.db.articles.find_one({'id': uid}, {'_id': False})
    convert.convert_article_format(article)
    return jsonify(article)


@api.route('/delete_article')
@login_required
def delete_article():
    uid = request.args['id']
    mongo.db.articles.update_one({'id': uid}, {'$set': {'status': 'deleted'}}, False)
    return jsonify({'status': 1})


@api.route('/get_all_articles')
@login_required
def get_articles_by_username():
    result = mongo.db.articles.find({'author.name': g.user.username}, {'_id': False, 'markdown': False, 'content': False})
    articles = list()
    for item in result:
        convert.convert_article_format(item)
        articles.append(item)
    return jsonify(articles)


@api.route('/recovery_deleted_article')
@login_required
def recover_deleted_article():
    uid = request.args['id']
    mongo.db.articles.update_one({'id': uid}, {'$set': {'status': 'published'}}, False)
    return jsonify({'status': 1})


@api.route('/get_user_list')
@login_required
def get_user_list():
    result = mongo.db.admins.find({}, {'_id': False, 'cryptPassword': False})
    user_list = list(result)
    return jsonify({'list': user_list, 'total': len(user_list)})


@api.route('/set_article_status', methods=['POST'])
@login_required
def set_article_status():
    jsondata = request.json
    uid = jsondata['id']
    status = jsondata['status']
    if check.verify_article_status(status):
        mongo.db.articles.update_one({'id': uid, 'author.username': g.user.username}, {'$set': {'status': status}})
        return jsonify({'status': 1})
    else:
        # status not allowed
        return jsonify({'status': 1})


@api.route('/get_article_list')
@login_required
def get_article_list():
    args = request.args
    page = args.get('page', 1)
    size = args.get('size', 10)
    result = convert.paginate(mongo.db.articles.find({}, {'_id': False, 'content': False, 'markdown': False}), page, size)
    articles = list(result)
    for item in articles:
        convert.convert_article_format(item)
        item['author'] = item['author']['username']
    return jsonify({'list': articles, 'total': len(articles)})


@api.route('/set_user_status', methods=['POST'])
@login_required
def set_user_status():
    jsondata = request.json
    uid = jsondata['id']
    status = jsondata['status']
    if check.verify_user_status(status):
        mongo.db.admins.update_one({'id': uid}, {'$set': {'status': status}})
        return jsonify({'status': 1})
    else:
        # status not allowed
        return jsonify({'status': 0})


@api.route('/edit_user', methods=['POST'])
@login_required
def edit_user():
    # TODO 更改用户名后，其他地方需要同步数据
    jsondata = request.json
    username = jsondata['name']
    try:
        mongo.db.admins.update_one({'username': g.user.username}, {'$set': {'username': username}})
    except DuplicateKeyError:
        return jsonify({'status': 0, 'msg': 'username:{} has been registered'.format(username)})
    else:
        return jsonify({'status': 1})


@api.route('/get_user_by_name')
@login_required
def get_user_by_name():
    args = request.args
    username = args['username']
    user = mongo.db.admins.find_one({'username': username}, {'_id': False, 'cryptPassword': False})
    convert.convert_user_format(user)
    articles = mongo.db.articles.find({'author.id': user['id']}, {'_id': False, 'title': True, 'id': True})
    user['articles'] = list(articles)
    return jsonify(user)


@api.route('/edit_article', methods=['POST'])
def edit_article():
    jsondata = request.json
    uid = jsondata['id']
    article = jsondata['article']
    mongo.db.articles.update_one({'id': uid}, article)
    return jsonify({'status': 1})
