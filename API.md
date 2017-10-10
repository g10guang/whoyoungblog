## 说明

文章状态 `status`

|    status    | 状态 |
| ---------- | --- |
| craft |  草稿 |
|  deleted   |  删除 |
| published | 发布 |

用户状态 `status`

|    status    | 状态 |
| ---------- | --- |
| frozen |  冻结   |
|  deleted   |  删除 |
| normal | 普通用户 |


所有 API 操作失败返回 `"-1"` 字符串

下面部分 URL 是有带域名的，部分是没有带域名的，商量后觉得是哪种方式更好，未来我进行统一更改。

> 假设一下域名均为 `domain.com` 


## 管理部分

### admin.domain.com

**response:**

返回管理后台前段管理页面

### admin.domain.com/login/

`POST`


登录接口

**request:**

```json
{
  "email": "g10guang@foxmail.com",
  "password": "hello world"
}
```

**response:**

登录成功返回  `"1"`；

登录失败返回  `"-1"`;


### admin.domain.com/upload/post

`POST`

上传博客

**request:**

```json
{
    "name": "post name",
    "tags": ["python", "go", "ruby", "perl"],
    "intro": "introduction of post",
    "content": "the content of markdown. large string."
}
```

**response:**

操作成功返回文章对应的 URL： `http://hello.com:5000/get_article/b1117bae43cb4adbadc77d3ffc9a9b77`

操作失败返回 `"-1"`

### admin.domain.com/upload/project

`POST`

上传项目

**request:**

```json
{
	"name": "hello world",
	"tags": ["hello", "world"],
	"author": ["g10guang"],
	"authorURL": ["https://github.com/g10guang"],
	"projectURL": "https://github.com/g10guang/whoyoungblog",
	"intro": "I want to say hello to the World.",
	"content": "the markdown of the project description"
}
```

**response:**

操作成功返回项目对应的 URL： `http://hello.com:5000/get_project/a2b5cd2750784ce4b41b816737827969`

操作失败返回 `"-1"`

### admin.domain.com/upload/navinfo

`POST`

修改导航栏条信息

**request:**

```json
{
  "homeTitle": "简",
  "navList": {
    "home": {
      "title": "字里行间",
      "text": "原谅我放荡不羁爱自由"
    },
    "projects": {
      "title": "字迹",
      "text": "存在"
    },
    "tags": {
      "title": "标签",
      "text": ""
    },
    "authors": {
      "title": "执笔",
      "text": "写尽"
    }
  }
}
```

**response:**

操作成功返回 `"1"`；

操作失败返回 `"-1"`；


## 对象存储

### domain.com/store/file

`POST`

**request:**

上传文件，具体文件在前段怎么上传我不是很清楚，但这个 API 目前来说只有上传文件这一个参数，对应的 key 为 name。测试时我是使用 form 表单提交。


**response:**

操作成功返回 `"/store/file/59c0df98461725211a3a1c55"`；

a操作失败返回 `"-1"`；

### domain.com/store/file/file_id

`GET`

通过文件唯一 id 获取文件

**response:**

file_id 正确返回文件；

file_id 错误返回 404


### domain.com/store/file/name/file_name

`GET`

不推荐使用该方法，因为后面上传的文件名会覆盖原来已经存在的文件名

但如果能够保证文件名不冲突，可以使用该方法

**response:**

file_name 正确返回文件；

file_name 错误返回 404

### domain.com/store/image

`POST`

**request:**

上传文件，具体图片在前段怎么上传我不是很清楚，但这个 API 目前来说只有上传文件这一个参数，对应的 key 为 image。测试时我是使用 form 表单提交。


**response:**

操作成功返回 `"/store/file/59c0df98461725211a3a1c55"`；

a操作失败返回 `"-1"`；

### domain.com/store/image/file_id

`GET`

通过文件唯一 id 获取文件

**response:**

file_id 正确返回文件；

file_id 错误返回 404


### domain.com/store/image/name/image_name

`GET`

不推荐使用该方法，因为后面上传的文件名会覆盖原来已经存在的文件名

但如果能够保证文件名不冲突，可以使用该方法

**request:**

不需要附带任何参数

**response:**

image_name 正确返回文件；

image_name 错误返回 404

> 推荐 image 和 file 分开使用，这样便于图片的管理，但是全部使用 /file 接口也是可以的。


## 展示

### domain.com

**response:**

返回前端页面
