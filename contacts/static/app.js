const bus = new Vue();

Vue.component('contacts', {
    props: ['tags'],
    template: `
    <div>
      <h2 v-if="! loading">{{people.length}} People</h2>
      <h2 v-if="loading">Loading...</h2>
      <p v-if="error">{{error}}</p>
      <p v-if="tagList.length">Tags chosen: <span v-for="(tag, index) in tagList"><span v-if="index > 0">, </span>{{tag}}</span></p>
      <div v-if="tagList.length"><button v-on:click="clearTags">Clear Tags</button></div>
      <table class="people" v-if="! loading">
        <thead>
          <tr>
            <th>Name</th>
            <th>Phones</th>
            <th>Email</th>
            <th>Zip</th>
            <th>Last Name</th>
            <th>Note</th>
          </tr>
        </thead>
        <tbody>
            <template v-for="(person, index) in people">
            <tr class="person" :key="person.id">
              <td class="name">
                  <a v-bind:href="person.href">{{ person.name }}</a>
              </td>
              <td class="phones">
                  <ul>
                    <li title="Mobile" v-if="person.mobile_phone">C: {{person.mobile_phone}}</li>
                    <li title="Home" v-if="person.home_phone">H: {{person.home_phone}}</li>
                    <li title="Work" v-if="person.work_phone">W: {{person.work_phone}}</li>
                </ul>
              </td>
              <td class="email">{{ person.email }}</td>
              <td class="zip">{{ person.zip_code }}</td>
              <td class="last_name">{{ person.last_name }}</td>
              <td class="show_note" v-if="person.note">
                  <button v-on:click="toggleNote(index)">
                      <span v-if="person.show_note">Hide</span>
                      <span v-else>Show</span>
                  </button>
              </td>
            </tr>

            <tr v-if="person.note && person.show_note" class="person" :key="person.id">
              <td></td>
              <td class="person note" colspan="4">{{person.note}}</td>
            </tr>

            <tr v-if="show_tags" class="person" :key="person.id">
              <td></td>
              <td class="person tags" colspan="4">
                <span class="tag" v-for="tag in person.tags">{{tag}}</span>
              </td>
            </tr>
          </template>
        </tbody>
      </table>
    </div>
    `,
    data: function() {
      const tags = []
      if (this.tags) {
        tags = this.tags.split(/, */);
      }
      return {
        people: [],
        show_tags: false,
        tagList: tags,
        error: undefined,
        loading: true,
      };
    },
    created: function() {
      this.refresh();
      const self = this;

      bus.$on('tag-selected', function (tag) {
        // Vue.set(this, 'tags', [tag]);
        self.tagList = [tag]
        console.log("Will attempt to show tags: ", self.tagList);
        self.refresh();
      })

    },
    methods: {
        toggleNote: function(index) {
            person = this.people[index];
            // console.log("Person:", person);

            person.show_note = ! person.show_note;
            // console.log("Person:", person);
        },
        refresh: function() {
          this.loading = true;
          console.log('Getting contacts...');
          // GET /someUrl
          this.$http.get('/api/contacts{?tag}', { params: { tag: [ this.tagList ] } }).then(response => {
            console.log("Got contacts:", response, response.body);
            // get body data
            this.people = response.body;
            this.people.forEach(function(item, index, array) {
              Vue.set(item, "show_note", false);
              Vue.set(item, "has_note", Boolean(item.note));
            });
            this.loading = false;
          }, response => {
            console.log("Error getting contacts:", response, response.body);
            this.error = response.body;
          });

      },
      clearTags: function() {
        this.tagList = [];
        this.refresh();
      },
    }
});

Vue.component('contact', {
    props: ['id'],
    template: `
    <div>
      <h2 v-if="person">{{person.name}}</h2>
      <p v-if="error">{{error}}</p>
      <table class="person" v-if="person">
        <tbody>
            <tr>
              <th>Name</th>
              <td class="name">
                  <a v-bind:href="person.href">{{ person.name }}</a>
              </td>
          </tr>
          <tr>
              <th>Cell Phone</th>
              <td class="phone">{{person.mobile_phone}}</td>
          </tr>
          <tr>
              <th>Home Phone</th>
              <td class="phone">{{person.home_phone}}</td>
          </tr>
          <tr>
              <th>Work Phone</th>
              <td class="phone">{{person.work_phone}}</td>
          </tr>
          <tr>
              <th>e-mail</th>
              <td class="email">{{ person.email }}</td>
          </tr>
          <tr>
              <th>Address</th>
              <td>
                <div v-for="note in lines(person.address)">{{note}}</div>
              </td>
          </tr>
          <tr>
              <th>Zip Code</th>
              <td class="zip">{{ person.zip_code }}</td>
          </tr>


    <!--
    TODO:
    active
    verified_on
    added_on
    created_at
    updated_at
    cached_tag_list
    -->


          <tr>
              <th>Last Name</th>
              <td>{{ person.last_name }}</td>
          </tr>
          <tr>
              <th>Note</th>
              <td>
                <p v-for="note in lines(person.note)">{{note}}</p>
              </td>
          </tr>

        </tbody>
      </table>
    </div>
    `,
    data: function() {
        return {
            person: undefined,
            error: undefined
        };
    },
    created: function() {
        console.log('Getting contacts...');
        // GET /someUrl
        this.$http.get('/api/contacts/' + this.id).then(response => {
            console.log("Got contact:", response, response.body);
            // get body data
            this.person = response.body;
        }, response => {
            console.log("Error getting contacts:", response, response.body);
            this.error = response.body;
        });
    },
    methods: {
        lines: function(text) {
            return text.split(/\r?\n/);
        },


    }
});



Vue.component('tags', {
    props: ['search'],
    template: `
    <div>
      <h2>{{tags.length}} Tags</h2>
      <p v-if="error">{{error}}</p>
      <ul class="tags">
          <li v-for="tag in tags">
              <a v-bind:href="tag.href" v-on:click.prevent="selectTag">{{tag.name}}</a>
          </li>
      </ul>
    </div>
    `,
    data: function() {
        return {
            tags: [],
            error: undefined
        };
    },
    created: function() {
        console.log('Getting contacts...');
        // GET /someUrl
        this.$http.get('/api/tags').then(response => {
            console.log("Got tags:", response, response.body);
            // get body data
            this.tags = response.body;
        }, response => {
            console.log("Error getting contacts:", response, response.body);
            this.error = response.body;
        });
    },
  methods: {
    selectTag: function(event) {
      console.log(event);
      console.log(event.srcElement.text);
      bus.$emit('tag-selected', event.srcElement.text);
    }
  }

});

