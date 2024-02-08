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

        await this.service.render();
        if (code != 200) return;
    }



} 
