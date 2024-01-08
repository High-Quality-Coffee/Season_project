import { OnInit, Input, NgModule, FormsModule } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';


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

    @Input() title: any;
    @Input text: string;
    @Input favorite: boolean;
    @Input newItem: string = '';

    items: ListItem[] = [];

    addItem() {
        if (this.newItem) {
            this.items.push({ text: this.newItem, favorite: false });
            this.newItem = '';
        }
    }

    toggleFavorite(item: ListItem) {
        item.favorite = !item.favorite;
    }
}