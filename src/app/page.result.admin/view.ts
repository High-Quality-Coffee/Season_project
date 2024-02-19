import { OnInit, Input } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Service } from '@wiz/libs/portal/season/service';
import { Menu } from '@wiz/libs/menu';

export class Component implements OnInit {
    @Input() title: any;
    public list: any;
    public score: any;


    public body = {
        sw: 'SW개발센터',
        rnd: 'R&D센터',
        season: '기술사업부'
    }

    constructor(
        public route: ActivatedRoute,
        public service: Service,
        public menu: Menu,
    ) { }

    public async ngOnInit() {
        this.onLoad();
    }

    public async onLoad() {
        const { code, data } = await wiz.call("search", this.body);
        this.list = data;
        await this.service.render();
        if (code != 200) return;

    }

    public async category(value) {
        let num;
        if ('sw' == value) num = this.body.sw;
        else if ('rnd' == value) num = this.body.rnd;
        else num = this.body.season;

        let obj = {
            category: num
        }

        const { code, data } = await wiz.call("category", obj);
        this.list = data;

        await this.service.render();
        if (code != 200) return;
    }

    public async input_score(val) {
        if (val != "close")
            document.getElementById("modal-score").style.display = "block";
        else if (val === "close") {
            document.getElementById("modal-score").style.display = "none";
            let input=document.getElementById("content-write");
            input.value=null;
        }
    }


}