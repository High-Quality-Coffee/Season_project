import { OnInit, Input } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Service } from '@wiz/libs/portal/season/service';
import { Menu } from '@wiz/libs/menu';


export class Component implements OnInit {
    @Input() title: any;
    public data: any = {
        center: 'dev'
    };

    public async ngOnInit() {
        
    }

    public list: '';

    public async data() {
        let user = JSON.parse(JSON.stringify(this.data));

        let { code, data } = await wiz.call("data", user);

        this.list = data;
        if (code == 200) return;


    }


}