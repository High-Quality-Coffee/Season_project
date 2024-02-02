import { OnInit, Input } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';

export class Component implements OnInit {
    constructor(public service: Service) { }

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
        interview: '',
        center: ''
    };

    public async ngOnInit() {
    }

    public async assign() {
        let user = JSON.parse(JSON.stringify(this.data));
        let { code, data } = await wiz.call("assign", user);
        if (code == 200) {
            await this.service.render();
            location.href = "result/admin";
            return;
        }

    }

}