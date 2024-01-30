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
        interview: ''
    };

    public async ngOnInit() {
    }

    public async save_userInfo() {
        let user = JSON.parse(JSON.stringify(this.data));
        let { code, data } = await wiz.call("save", user);
        if (code == 200) {
            await this.service.render();
            
            return;
        }
        
        location.href = "result/admin";
        
    }

}