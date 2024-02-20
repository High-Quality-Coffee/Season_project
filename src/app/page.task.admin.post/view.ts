import { OnInit, Input } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Service } from '@wiz/libs/portal/season/service';
import ClassicEditor from '@wiz/libs/ckeditor/ckeditor';

export class Component implements OnInit {
    public title: any;
    public editor;
    public post = { id: "", title: "", category: "", content: "", files: [] };
    public file;
    public fd = new FormData();
    public list: any;

    constructor(
        public route: ActivatedRoute,
        public service: Service,
    ) { }

    public async ngOnInit() {
        this.onLoad();
    }

    public async init() {
        this.post.id = WizRoute.segment.id;
        this.post.category = WizRoute.segment.category;
        this.title = this.category_list.find(e => e.id === this.post.category).name
        if (this.post.id !== "new") {
            const { code, data } = await wiz.call("load", { id: this.post.id });
            this.post = data;
            this.post.files = JSON.parse(data.files.replace(/'/g, '"'));
            await this.service.render();
        }
        else this.post.id = ""
        const EDITOR_ID = 'textarea#editor';
        this.editor = await ClassicEditor.create(document.querySelector(EDITOR_ID), {
            toolbar: {
                items: 'heading | bold italic strikethrough underline | fontColor highlight fontBackgroundColor | bulletedList numberedList todoList | outdent indent | insertTable imageUpload | link blockQuote code codeBlock'.split(' '),
                shouldNotGroupWhenFull: true
            },
            removePlugins: ["MediaEmbedToolbar", "Markdown"],
            table: ClassicEditor.defaultConfig.table,
            simpleUpload: {
                uploadUrl: '/file/upload/' + this.post.category + "/file"
            }
        });
        this.editor.data.set(this.post.content);
        await this.service.render();
    }

    public async update() {
        let post = this.post;
        post.content = this.editor.data.get();
        this.fd.append("data", JSON.stringify(post))
        let url = wiz.url('update')
        const { code, data } = await this.service.file.upload(url, this.fd);
        if (code === 200) {
            location.href = `/community/${this.post.category}/view/${data}`;
        }
        else alert("오류가 발생했습니다. 다시 시도해주세요.")
    }

    public async upload(e) {
        for (let i = 0; i < e.target.files.length; i++) {
            let file = e.target.files[i]
            if (!file.filepath) file.filepath = file.name;
            this.fd.append('file[]', file);
            this.post.files.push(file.filepath);
        }
        await this.service.render();
    }

    public async delete_file(item) {
        let files = this.post.files
        let index = files.indexOf(item);
        files.splice(index, 1)
        this.post.files = files;
        await this.service.render();
        // if (!this.post.id) return;

        // let body = { id: this.post.id, item: item }
        // let { code, data } = await wiz.call("delete_file", body);
        // if (code != 200) {
        //     alert("새로고침 후 다시 삭제해주세요.");
        // }
    }

    public async delete() {
        // let res = await alert("게시글을 삭제하면 복원할 수 없습니다. 정말 삭제하시겠습니까?", { title: "게시글 삭제", btn_action: "삭제", btn_close: "취소" });

        await wiz.call('delete', { id: this.post.id });
        alert("삭제되었습니다.");
        this.go(this.post.category);
    }


    public async onLoad() {
        let index = window.localStorage.getItem("title");
        const { code, data } = await wiz.call("onLoad", { title: index });
        this.post = data;

        // 에디터 붙이기
        const EDITOR_ID = 'textarea#editor';
        this.editor = await ClassicEditor.create(document.querySelector(EDITOR_ID), {
            toolbar: {
                items: 'heading | bold italic strikethrough underline | fontColor highlight fontBackgroundColor | bulletedList numberedList todoList | outdent indent | insertTable imageUpload | link blockQuote code codeBlock'.split(' '),
                shouldNotGroupWhenFull: true
            },
            removePlugins: ["MediaEmbedToolbar", "Markdown"],
            table: ClassicEditor.defaultConfig.table,
            simpleUpload: {
                uploadUrl: '/file/upload/' + this.post.category + "/file"
            }
        });
        this.editor.data.set(this.post.content);

        await this.service.render();
        if (code != 200) return;
    }



} 
