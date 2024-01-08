import { OnInit, Input, NgModule, Component } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';


export class Component implements OnInit {
    // @NgModule({
    //     declarations: [
    //         AppComponent
    //     ],
    //     imports: [
    //         BrowserModule,
    //         FormsModule
    //     ],
    //     providers: [],
    //     bootstrap: [AppComponent],
    // })

    // @Input() title: any;
    // @Input text: string;
    // @Input favorite: boolean;
    // @Input newItem: string = '';

    public title: any;
    public text: string;
    public favorite: boolean;
    public newItem: string = '';

    public items: ListItem[] = [];

    public async addItem(newItem) {
        if (this.newItem) {
            this.items.push({ text: this.newItem, favorite: false });
            console.log(items)
            this.newItem = '';
        }
    }

    public async toggleFavorite(item: ListItem) {
        item.favorite = !item.favorite;
    }
}

