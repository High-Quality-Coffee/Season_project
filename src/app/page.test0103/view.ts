import { OnInit, Input, NgModule } from '@angular/core';

export class Component implements OnInit {
    @Input() title: any;

    public newItem = [];

    public async addItem() {
        if (this.name && this.password) {
            newItem.push({ title: this.name, text: this.password });
            this.name = '';
            this.password = '';
        }
        console.log(newItem);
    }


    public async ngOnInit() {
    }
}