import { OnInit, Input } from '@angular/core';

export class Component implements OnInit {
    @Input() title: any;
    public modalOpenButton: any;
    public modalCloseButton: any;
    public modal: any;


    public async ngOnInit() {
        this.modal = document.getElementById('modalContainer');
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