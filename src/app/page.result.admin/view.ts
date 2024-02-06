import { OnInit, Input } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Service } from '@wiz/libs/portal/season/service';
import { Menu } from '@wiz/libs/menu';

export class Component implements OnInit {
    @Input() title: any;
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
        let body = {
            center: 'dev',
        }
        const { code, data } = await wiz.call("search", body);
        this.list = data;
        console.log(this.list);
        await this.service.render();
        if (code != 200) return;

    }


}