import { OnInit, Input } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Service } from '@wiz/libs/portal/season/service';
import { Menu } from '@wiz/libs/menu';

export class Component implements OnInit {
    public items: any;

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
        //let list = JSON.parse(data[0].assignName);
        let body = {
            list: data[0].assignName
        }
        await this.service.render();

        const { coding, dating } = await wiz.call("onLoading", body);
        this.items = dating;
        await this.service.render();
        console.log(dating);
        if (code != 200) return;
    }

    public async saveTitle(value) {
        window.localStorage.setItem('title', value);
    }

}
