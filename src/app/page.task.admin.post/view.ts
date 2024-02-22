import { OnInit, Input } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Service } from '@wiz/libs/portal/season/service';
import ClassicEditor from '@wiz/libs/ckeditor/ckeditor';

export class Component implements OnInit {
    public title: any;
    public user;
    public category_list = [{ id: "notice", name: "공지사항" }, { id: "request", name: "요청사항" }, { id: "free", name: "자유게시판" }];
    public post = { id: "", category: "", content: "", user: {} };
    public comment = { community_id: this.post.id, content: "" };
    public comments;
    public edit_comment: boolean = false;
    public editor;

    constructor(
        public route: ActivatedRoute,
        public service: Service,
    ) { }

    public async ngOnInit() {
        await this.service.init();
        await this.load();
    }

    public async load() {
        this.post.id = WizRoute.segment.id;
        let { code, data } = await wiz.call('load', { id: this.post.id })
        if (code !== 200) {
            alert("로드실패. 다시 시도해주세요.")
        }
        this.post = data.post;
        this.post.files = JSON.parse(data.post.files.replace(/'/g, '"'));
        this.user = data.user;
        this.comment.community_id = this.post.id;
        this.title = this.category_list.find(e => e.id === this.post.category).name
        await this.load_comment();

        const EDITOR_ID = 'textarea#editor';
        this.editor = await ClassicEditor.create(document.querySelector(EDITOR_ID), {})
        this.editor.isReadOnly = true;
        this.editor.data.set(this.post.content);
        this.editor.ui.view.toolbar.element.style.display = 'none';
        await this.service.render();
    }

    public async load_comment() {
        let { code, data } = await wiz.call('comment', { post_id: this.post.id })
        this.comments = data;
        await this.service.render;
    }

    public go(item) {
        const obj = {
            category: item,
        }
        this.service.href([`/community/list`, obj]);
    }

    public async edit() {
        this.service.href(`/community/${this.post.category}/edit/${this.post.id}`);
    };

    public async create() {
        let comment = this.comment;
        let { code, data } = await wiz.call('create', comment)
        if (code === 200) this.comment = { post_id: this.post.id, content: "" };
        await this.load();
    };
    public async delete(comment) {
        let { code, data } = await wiz.call('delete', { id: comment.id })
        location.reload();
    };
    public async update(item) {
        let { code, data } = await wiz.call('update', item)
        location.reload();
    };
} 
