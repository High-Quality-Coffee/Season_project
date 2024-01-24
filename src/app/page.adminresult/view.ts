import { OnInit, Input } from '@angular/core';

export class Component implements OnInit {
    @Input() title: any;
    public modalOpenButton: any;
    public modalCloseButton: any;
    public modal: any;
    public selected: "";
    public isShow: any;


    public async ngOnInit() {
        this.modal = document.getElementById('modalContainer');
        this.isShow = true;
    }

    public async modal_remove() {
        if (this.modal) {
            this.modal.classList.remove('hidden');
        }
    }

    public async modal_add() {
        if (this.modal)
            this.modal.classList.add('hidden');
    }


    public async changeOption(option) {
        this.isShow = false;
        if (this.option == 'accept') this.selected = option;
        else this.selected = option;
    }

    public async choiceAgain() {
        this.isShow = true;
        this.selected = "";
        if (this.modal) this.modal.classList.add('hidden');
    }


}