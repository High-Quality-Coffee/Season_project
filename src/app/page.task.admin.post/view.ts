import { OnInit, Input } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Service } from '@wiz/libs/portal/season/service';
import ClassicEditor from '@wiz/libs/ckeditor/ckeditor';

export class Component implements OnInit {
    public post: any = {
        id: '',
        title: '',
        content: ''
    };

    constructor(
        public route: ActivatedRoute,
        public service: Service,
    ) { }

    public async ngOnInit() {
        this.onLoad();
    }

    public async onLoad() {
        let index = window.localStorage.getItem("title");
        const { code, data } = await wiz.call("onLoad", { title: index });
        console.log(data);
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
