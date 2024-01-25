import { OnInit, Input } from '@angular/core';
import { Service } from "@wiz/libs/portal/season/service";

export class Component implements OnInit {
    @Input() title: any;
    public moveCheck: any;

    public async ngOnInit() {


    }


    public async moveTaskNotice() {
        this.moveCheck = window.localStorage.getItem('moveItem');
        
        if (this.moveCheck == "moveAdmin")
            location.href = "/AdminTaskNotice"
        else
            location.href = "/UserTaskNotice"


        //await this.service.render();
    }


}