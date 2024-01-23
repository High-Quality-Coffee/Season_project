import { OnInit, Input } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Service } from '@wiz/libs/portal/season/service';
import { Menu } from '@wiz/libs/menu';

export class Component implements OnInit {
    public list: [];

    public page = {
        start: 1,
        end: 1,
        current: 1,
    };
    public text: string = "";
    public category: string;
    public title: string = "";
    public category_list = [{ id: "notice", name: "공지사항" }, { id: "request", name: "요청사항" }, { id: "free", name: "자유게시판" }];

    constructor(
        public route: ActivatedRoute,
        public service: Service,
        public menu: Menu,
    ) { }

    public async ngOnInit() {
        await this.service.init();
        this.route.params.subscribe(async ({ category }) => {
            this.category = category;
            this.pageLoad(1);
        })
    }
    public go(item) {
        const obj = {
            category: item,
        }
        this.service.href([`/community/list`, obj]);
    }

    private pageLoad(p: number) {
        this.page.current = p;
        this.onLoad();
    }

    public async onLoad() {
        this.title = this.category_list.find(e => e.id === this.category).name
        let body = {
            category: this.category,
            page: this.page.current,
        };
        // if (body.text.replace(/\s/g, "").length === 0) delete body.text;
        const { code, data } = await wiz.call("search", body);
        if (code !== 200) return;
        const { list, lastpage } = data;
        this.page.start = (parseInt(this.page.current / 11) * 10) + 1;
        this.page.end = lastpage;
        this.list = list;
        await this.service.render();
    }

     public async move(){
        location.href="/AdminResult";
    }


    // public async search() {
    //     this.query.page = 1;
    //     var q = thisect.entries(angular.copy(this.query)).map(e => e.join('=')).join('&');
    //     location.href = "?" + q;
    // }
}
