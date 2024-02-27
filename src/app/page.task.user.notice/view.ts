import { OnInit, Input } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Service } from '@wiz/libs/portal/season/service';
import { Menu } from '@wiz/libs/menu';

export class Component implements OnInit {
    public items: any;
    public body: any;
    public pubdata: any;
    public duedates: any;

    constructor(
        public route: ActivatedRoute,
        public service: Service,
        public menu: Menu,
    ) { }

    public async ngOnInit() {
        this.onLoad();
        await this.service.init();
    }

    public async onLoad() {
        let email = {
            email: window.localStorage.getItem('email')
        }
        const { code, data } = await wiz.call("onLoad", email);
        this.pubdata = data[0].assignName;
        this.duedates=data[0].duedate;
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
        if (coding != 200) return;
        await this.service.render();
    }

    public async saveTitle(value) {
        window.localStorage.setItem('title', value);
    }

    public async logout(val='open') {
        if (val == "open") {
            document.getElementById("modal-score").style.display = "block";
        }
        else if (val == "close") {
            document.getElementById("modal-score").style.display = "none";
        }
        else if (val === "logout") {
            location.href="/login";
        }
    }

}
