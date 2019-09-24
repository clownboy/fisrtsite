var vm = new Vue({
    el: "#app",
    data: {
        repassword:'',
        comments:[],
        artical: {
            bookname: '',
            author: '',
            content: '',
            page: '',
            noteid: '',
        },
        email:'',
        commenttext:'',
        commentpage: '',
        alertVisible: false,
        noteloading: false,
        dialogVisible: false,
        notepage: false,
        nickname: '',
        flag: true,
        notenumber: '0',
        shownumber: {
            show: false,
        },
        loading: {
            show: false,
        },
        doubanapi: '',
        doubanID: '',
        headpage: {
            show: false,
        },
        copypage: {
            show: false,
        },
        account: {
            show: false,
        },
    },
    filters: {
        formatDate: function(value) {
            let date = new Date(value);
            let y = date.getFullYear();
            let MM = date.getMonth() + 1;
            MM = MM < 10 ? ('0' + MM) : MM;
            let d = date.getDate();
            d = d < 10 ? ('0' + d) : d;
            let h = date.getHours();
            h = h < 10 ? ('0' + h) : h;
            let m = date.getMinutes();
            m = m < 10 ? ('0' + m) : m;
            let s = date.getSeconds();
            s = s < 10 ? ('0' + s) : s;
            return y + '-' + MM + '-' + d + ' ' +h + ': '+m + ': '+s;
        }
    },
    methods: {
        emailSet(){
          if(/^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/.test(this.email)){
          url = 'https://brokenstory.club/emailset'
          var formData = new FormData()
          formData.append("email", this.email)
          this.$http.post(url, formData, {
              headers: {
                  'X-CSRFToken': this.getCookie('csrftoken')
              }
          }).then(function(res){
            console.log(res.body.error)
                 if (res.body.error){
                  alert('提交失败，该邮箱已被使用');
                }else{
                  alert('提交成功，登陆邮箱确认');
                }
              })}else{
          alert('邮箱格式错误');
        }
        },
        passwordSet(){
          var password=this.repassword
          if(srt(password).length < 6 ){
              alert('密码必须大于6位')
            }else{
              url = 'https://brokenstory.club/passwordset'
              var formData = new FormData()
              formData.append("repassword", password)
              this.$http.post(url, formData, {
                  headers: {
                      'X-CSRFToken': this.getCookie('csrftoken')
                  }
              }).then(function(res){
                   alert('密码修改成功,需重新登陆');
                   window.location.href = "https://brokenstory.club"
                 },function(){
                   alert('密码修改失败')
                 })
           }
        },
        talk(){
          url = 'https://brokenstory.club/comment'
          var formData = new FormData()
          formData.append("talk", this.commenttext)
          formData.append("artical", this.commentpage)
          this.$http.post(url, formData, {
              headers: {
                  'X-CSRFToken': this.getCookie('csrftoken')
              }
          }).then(function(res) {
              if (res.ok) {
                  window.location.reload()
              } else {
                  console.log("not ok")
              }
          })
        },
        closecomment(){
          this.commentpage = 0;
          this.commentext = '';
        },
        comment(id) {
                this.commentpage = id;
                url = 'https://brokenstory.club/api/getcomment'
                this.$http.get(url, {
                    params: {id}
                }).then(function(res) {
                    if (res.ok) {
                        this.comments = res.body
                        console.log(res.body)
                    } else {
                        console.log("not ok")
                    }
                })
        },
        handleInput(e) {
            this.artical.page = e.target.value.replace(/[^\d]/g, '');
        },
        deletenote(noteid) {
            var r = confirm("是否确定删除？")
            if (r == true) {
                url = 'https://brokenstory.club/deletenote'
                this.$http.post(url, noteid, {
                    headers: {
                        'X-CSRFToken': this.getCookie('csrftoken')
                    }
                }).then(function(res) {
                    if (res.ok) {
                        window.location.reload()

                    } else {
                        console.log("not ok")
                    }
                })
            } else {
                return false
            }
        },
        onNote() {
            this.noteloading = true;
            if (this.artical.bookname && this.artical.content) {
                var formData = new FormData()
                url = 'https://brokenstory.club/onnote'
                if (this.artical.noteid) {
                    formData.append("id", this.artical.noteid)
                }
                formData.append("bookname", this.artical.bookname)
                formData.append("author", this.artical.author)
                formData.append("content", this.artical.content)
                formData.append("pagenumber", this.artical.page)
                this.$http.post(url, formData, {
                    headers: {
                        'X-CSRFToken': this.getCookie('csrftoken')
                    }
                }).then(function(res) {
                    res = res.body.resp
                    if ("error" == res) {
                        alert('信息有误');
                    } else {
                        console.log("ok")
                        window.location.reload()
                    }
                })
            } else {
                alert('信息不完整');
                this.noteloading = false;
            }
        },
        editnote(id) {
            this.dialogVisible = true;
            if (id) {
                bookname = document.getElementById("bookname" + id).innerHTML;
                this.artical.bookname = bookname.slice(1, -1);
                this.artical.author = document.getElementById("author" + id).innerHTML;
                this.artical.content = document.getElementById("content" + id).innerHTML;
                num = document.getElementById("page" + id).innerHTML;
                this.artical.page = num.slice(1, -1);
                this.artical.noteid = id;
            } else {
                this.artical.bookname = '';
                this.artical.author = '';
                this.artical.content = '';
                this.artical.page = '';
                this.artical.noteid = 0;
            }
        },
        gonumpage(x) {
            window.location.href = "https://brokenstory.club/mynote" + "?page=" + x
        },
        outchange() {            
            this.flag = true;
        },
        changename() {
            var formData = new FormData()
            url = 'https://brokenstory.club/account'
            formData.append("nickname", this.nickname)
            this.$http.post(url, formData, {
                headers: {
                    'X-CSRFToken': this.getCookie('csrftoken')
                }
            }).then(function(res) {
                if (res.ok) {
                    console.log(res.body)
                    this.flag = true;
                    location.reload()
                } else {
                    this.flag = true;
                    console.log("not ok")
                }
            })
            this.flag = true;
        },
        editnickname() {
            this.flag = false;
        },
        IDclean: function() {
            Id = this.doubanID;
            this.loading.show = true;
            var reg = new RegExp("[\\u4E00-\\u9FFF]+", "g");
            if (Id.length == 0 || reg.test(Id)) {
                alert('用户名无效');
                document.getElementById("dbid").value = "";
                this.loading.show = false;
                return
            } else {
                this.doubanapi = 'https://api.douban.com/v2/book/user/' + Id + '/annotations?apikey=0df993c66c0c636e29ecbb5344252a4a';
                this.$http.jsonp(this.doubanapi).then(function(res) {
                    if (res.ok) {
                        sum = res.body.total
                        this.onCopy(sum);
                    }
                }, function() {
                    alert('请求失败，请检查用户名是否正确');
                    this.loading.show = false;
                });
            }
        },
        onCopy: function(total) {
            doubanapi = this.doubanapi + '&count=' + total;
            this.$http.jsonp(doubanapi).then(function(res) {
                if (res.ok) {
                    var getData = res.body.annotations;
                    for (var i in getData) {
                        this.notenumber++;
                        this.noteList(getData[i].book.title, getData[i].book.author, getData[i].content, getData[i].page_no, getData[i].time)
                    }
                    alert('搬运完成，一共' + res.body.total + '条笔记');
                    window.location.href = "https://brokenstory.club/mynote?page=1"
                    this.loading.show = false;
                }
            }, function() {
                alert('搬运失败，可能笔记较多或者服务问题,请稍后再试');
                this.loading.show = false;
                return false;
            })
        },
        getCookie(name) {
            var value = '; ' + document.cookie
            var parts = value.split('; ' + name + '=')
            if (parts.length === 2) return parts.pop().split(';').shift()
        },
        contclean(str) {
            if (str.substring(2, 7) == 'block') {
                var str = str.slice(99, -19);
            }
            str = str.replace(/("\},\{).*?(text":")|(",").*?(text":")|(",").*?(\}\}\]\})|({"en).*?(text":")/g, "");
            var reg = RegExp(/"src":"https:/);
            if (reg.test(str)) {
                str = "原笔记为图片，暂不支持"
            }
            return str
        },

        noteList(bookname, author, content, pagenumber, notetime) {
            var cont = this.contclean(content)
            var formData = new FormData()
            url = 'https://brokenstory.club/onnote'
            formData.append("bookname", bookname)
            formData.append("author", author)
            formData.append("content", cont)
            formData.append("pagenumber", pagenumber)
            formData.append("notetime", notetime)
            this.$http.post(url, formData, {
                headers: {
                    'X-CSRFToken': this.getCookie('csrftoken')
                }
            }).then(function(res) {
                res = res.body.resp
                if ("error" == res) {
                    alert('信息有误');
                } else {
                    console.log("ok")
                    window.location.href = "https://brokenstory.club/mynote?page=1"
                }
            })
        },
        noteCopy: function() {
            this.copypage.show = !this.copypage.show

        },
        setting: function() {
            this.account.show = !this.account.show
        },
        headlogo: function() {
            this.headpage.show = !this.headpage.show
        }
    },
})
