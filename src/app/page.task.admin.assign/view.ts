import { OnInit, Input } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Service } from '@wiz/libs/portal/season/service';
import ClassicEditor from '@wiz/libs/ckeditor/ckeditor';
import { Menu } from '@wiz/libs/menu';


export class Component implements OnInit {
    constructor(public service: Service) { }

    public list: any;

    public async ngOnInit() {
        await this.service.init();
        // await this.service.auth.allow(false, '/main');
    }

    @Input() title: any;
    public data: any = {
        id: '',
        name: '',
        email: '',
        phone: '',
        assignName: new Array(),
        interview: '',
        duedate: '',
        center: ''
    };

    public async ngOnInit() {
        this.onLoad();
        await this.service.init();
    }

    public async assign() {
        //let user = JSON.parse(JSON.stringify(this.data));
        this.data.assignName=JSON.stringify(this.data.assignName);
        let user = this.data;
        let { code, data } = await wiz.call("assign", user);
        if (code == 200) {
            await this.service.render();
            location.href = "result/admin";
            return;
        }

    }

    public async saveAssign(value) {
        //let { code, data } = await wiz.call("saveAssign", { assignName: value });
        this.data.assignName.push(value);
    }

    public async onLoad() {
        let body = {
            email: 'test'
        }
        const { code, data } = await wiz.call("onLoad", body);
        this.list = data;
        await this.service.render();
        if (code != 200) return;
    }
}