import { OnInit, Input } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Service } from '@wiz/libs/portal/season/service';
import { Menu } from '@wiz/libs/menu';

export class Component implements OnInit {
    public items: any;
    public body: any;
    public pubdata: any;
    public duedates: any;
    public files: any;

    constructor(
        public route: ActivatedRoute,
        public service: Service,
        public menu: Menu,
    ) { }

    public async ngOnInit() {
        await this.service.init();
        this.onLoad();
        this.fileCheck();
        await this.service.render();
    }

    public async fileCheck() {
        let body = {
            email: window.localStorage.getItem('email'),
            title: window.localStorage.getItem('title')
        };
        const { code, data } = await wiz.call("fileCheck", body);
        if (code != 200)
            return;
        this.files = data;
        await this.service.render();
    }


    public async onLoad() {
        let email = {
            email: window.localStorage.getItem('email')
        }
        const { code, data } = await wiz.call("onLoad", email);
        this.pubdata = data[0].assignName;
        this.duedates = data[0].duedate;
        //let list = JSON.parse(data[0].assignName);
        this.body = {
            list: this.pubdata
        }
        if (code != 200)
            return;
        await this.service.render();
        this.onLoading();
    }

    public async onLoading() {
        const { code, data } = await wiz.call("onLoading", this.body);
        this.items = data;
        await this.service.render();
        if (code != 200) return;
    }

    public async saveTitle(value) {
        window.localStorage.setItem('title', value);
        await this.service.render();
        location.href = "/task/user/post";
    }

    public async logout(val = 'open') {
        if (val == "open") {
            document.getElementById("modal-score").style.display = "block";
        }
        else if (val == "close") {
            document.getElementById("modal-score").style.display = "none";
        }
        else if (val === "logout") {
            location.href = "/login";
        }
    }

    public async movetoNext() {
        await this.service.render();
        location.href = "/result/user";
    }
}
