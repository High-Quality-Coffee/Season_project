import { OnInit } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';

export class Component implements OnInit {
    constructor(public service: Service) { }
    public async ngOnInit() {
        await this.service.init();
        // await this.service.auth.allow(false, '/main');
    }

    public status: any = false;
    public password2: string = '';
    public data: any = {
        email: '',
        id: '',
        password: '',
        name: ''
    };

    public async alert(message: string, status: string = 'error') {
        return await this.service.alert.show({
            title: "",
            message: message,
            cancel: false,
            actionBtn: status,
            action: "확인",
            status: status
        });
    }

    public async submit() {
        let user = JSON.parse(JSON.stringify(this.data));
        //user.password = this.service.auth.hash(user.password);
        let { code, data } = await wiz.call("submit", user);
        console.log(data);
        if (code == 200) {
            await this.service.render();
            location.href = "/auth/login"
            return;
        }
        //await this.alert(this.data);
    }
}