import { OnInit, Input } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Service } from '@wiz/libs/portal/season/service';
import { Menu } from '@wiz/libs/menu';

export class Component implements OnInit {
    @Input() title: any;
    public list: [];

    constructor(
        public route: ActivatedRoute,
        public service: Service,
    ) { }

    public async ngOnInit() {
        await this.service.init();
        this.pageLoad(1);
    }

    private pageLoad() {
        this.onLoad();
    }

    public async onLoad() {
        let body = {
            category: 'category'
        }
        const { code, list } = await wiz.call("search", body);
        console.log(list);
        if (code != 200) return;

        this.list = list;
        await this.service.render();

    }


}