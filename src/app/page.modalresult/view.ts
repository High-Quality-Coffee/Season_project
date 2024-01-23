import { OnInit, Input } from '@angular/core';
import { Service } from "@wiz/libs/portal/season/service";

export class Component implements OnInit {
    @Input() title: any;
    public modalOpenButton: any;
    public modalCloseButton: any;
    public modal: any;

    constructor() { }

    public async ngOnInit() {
        this.modal = document.getElementById('modalContainer');
        await this.service.init();
        await this.load();
    }

    public async modal_remove() {
        if (this.modal)
            this.modal.classList.remove('hidden');
    }

    public async modal_add() {
        if (this.modal)
            this.modal.classList.add('hidden');
    }

}