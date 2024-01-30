import { OnInit, Input } from '@angular/core';
import { Service } from "@wiz/libs/portal/season/service";

export class Component implements OnInit {
    @Input() title: any;
    public moveItem: any;

    constructor() { }

    public async ngOnInit() {
        await this.service.init();
        await this.load();
    }

    public async move(moveItem) {
        this.moveItem = moveItem;

        if (this.moveItem == 'moveAdmin') {
            localStorage.setItem('moveItem', 'moveAdmin');
            location.href = "/login"
            
        }
        else {
            localStorage.setItem('moveItem', 'moveUser');
            location.href = "/login"
            
        }
        await this.service.render();
    }
}