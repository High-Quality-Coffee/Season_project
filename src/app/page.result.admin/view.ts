import { OnInit, Input } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Service } from '@wiz/libs/portal/season/service';
import { Menu } from '@wiz/libs/menu';

export class Component implements OnInit {
    @Input() title: any;
    public list: any;
    public score: any;
    public email: any;
    public center_category: any;



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
        this.centerLoad();
    }

    public async onLoad() {
        const { code, data } = await wiz.call("search", this.body);
        this.list = data;
        this.center_category = "전체보기";
        await this.service.render();
        if (code != 200) return;

    }

    public async centerLoad() {
        let center = window.localStorage.getItem("center");
        this.center_category = center;
        if (center === 'SW개발센터')
            this.category("sw");
        else if (center === '기술사업부')
            this.category("season");
        else if (center === 'R&D센터')
            this.category("rnd");
    }

    public async category(value) {
        let num;
        if ('sw' == value) {
            num = this.body.sw;
            this.center_category = num;
        }
        else if ('rnd' == value) {
            num = this.body.rnd;
            this.center_category = num;
        }
        else {
            num = this.body.season;
            this.center_category = num;
        }

        let obj = {
            category: num
        }

        const { code, data } = await wiz.call("category", obj);
        this.list = data;

        await this.service.render();
        if (code != 200) return;
    }

    public async input_score(val) {
        if (val != "close" && val != "save") {
            document.getElementById("modal-score").style.display = "block";
            this.email = val;
        }
        else if (val === "close") {
            document.getElementById("modal-score").style.display = "none";
            let input = document.getElementById("content-write");
            input.value = null;
        }
        else if (val === "save") {
            const { code, data } = await wiz.call("save", { score_obj: this.score, email_obj: this.email });
            document.getElementById("modal-score").style.display = "none";
            let input = document.getElementById("content-write");
            input.value = null;

            if (data === 'SW개발센터')
                this.category("sw");
            else if (data === '기술사업부')
                this.category("season");
            else if (data === 'R&D센터')
                this.category("rnd");
            await this.service.render();

            if (code != 200) return;
        }
    }

    public async input_feedback(val) {
        this.email = val;
        window.localStorage.setItem("user_email", this.email);
        location.href = "task/admin/feedback";

    }

    public async logout(val = 'open') {
        if (val == "open") {
            document.getElementById("modal-sec").style.display = "block";
        }
        else if (val == "close") {
            document.getElementById("modal-sec").style.display = "none";
        }
        else if (val === "logout") {
            location.href = "/login";
        }
    }


}