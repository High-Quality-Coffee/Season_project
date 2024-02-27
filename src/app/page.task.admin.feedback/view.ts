import { OnInit, Input } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Service } from '@wiz/libs/portal/season/service';
import { Menu } from '@wiz/libs/menu';

export class Component implements OnInit {
    public list: any;


    constructor(
        public route: ActivatedRoute,
        public service: Service,
        public menu: Menu,
    ) { }

    public async ngOnInit() {
        this.onLoad();
    }

    public async onLoad() {
        let email = window.localStorage.getItem("user_email");
        const { code, data } = await wiz.call("onLoad", { user_email: email });
        if (data.length == 0)
            this.list = undefined;
        else
            this.list = data;
        console.log(this.list);

        await this.service.render();
        if (code != 200) return;
    }

    public send_title(val) {
        window.localStorage.setItem("fdb_title",val);
    }

}