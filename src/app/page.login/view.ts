import { OnInit } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';
import { Menu } from '@wiz/libs/menu';

export class Component implements OnInit {
    public moveCheck: any;

    constructor(
        public service: Service,
        public menu: Menu,
    ) { }

    public async ngOnInit() {
        await this.service.init();
        await this.service.render();
    }

    public data: any = {
        email: '',
        password: '',
    };

    public async moveTaskNotice() {
        this.moveCheck = window.localStorage.getItem('moveItem');

        if (this.moveCheck == "moveAdmin")
            location.href = "/task/admin/notice"
        else
            location.href = "/task/user/notice"


        //await this.service.render();
    }

    public async alert(message: string, status: string = 'error') {
        alert(message);
    }

    public async login() {
        let user = JSON.parse(JSON.stringify(this.data));

        let { code, data } = await wiz.call("login", user);
        if (code !== 200) {
            this.alert(data);
            return;
        }
        localStorage.setItem('email', this.data.email);
        if (data == "admin")
            location.href = "/task/admin/notice"
        else
            location.href = "/task/user/notice"

    }
}