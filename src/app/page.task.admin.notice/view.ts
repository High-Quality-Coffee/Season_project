import { OnInit, Input } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Service } from '@wiz/libs/portal/season/service';
import { Menu } from '@wiz/libs/menu';

export class Component implements OnInit {
    public list: [];

    // 맨 끝 대문자 코드, 함수, 변수 테스트용으로 작성
    public lisT: any;

    public page = {
        start: 1,
        end: 1,
        current: 1,
    };

    constructor(
        public route: ActivatedRoute,
        public service: Service,
        public menu: Menu,
    ) { }

    public async ngOnInit() {
        this.onLoaD();
        await this.service.init();
    }

    public async onLoaD() {
        let user = window.localStorage.getItem('email');
        let body = {
            email: user,
        }
        const { code, data } = await wiz.call("onLoaD", body);
        this.lisT = data;
        await this.service.render();
        if (code != 200) return;
    }

    public async saveTitle(value) {
        window.localStorage.setItem('title', value);
    }

}
