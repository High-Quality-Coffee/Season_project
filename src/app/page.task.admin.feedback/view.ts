import { OnInit, Input } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Service } from '@wiz/libs/portal/season/service';
import { Menu } from '@wiz/libs/menu';

export class Component implements OnInit {
    constructor(
        public route: ActivatedRoute,
        public service: Service,
        public menu: Menu,
    ) { }

    public async ngOnInit() {
        
    }

    


}