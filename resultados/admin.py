class ConfigAdmin(admin.ModelAdmin):   

    list_display = ('id', 'username', 'useralias','status','language','action')
    

    def get_urls(self):

        urls = (superConfigAdmin, self).get_urls()

        my_urls = patterns('',

                          (r'^view/(?P\d+)', self.admin_site.admin_view(self.config_detail))

        )

        return my_urls + urls

 

    def config_detail(self,request, id):

        config = Config.objects.get(pk=id),exclude.('email_notification', 'loginkey'))

        opts = Config._meta

        app_label = opts.app_label


        #create tempate page and extend admin/base.html

        config_detail_view_template = 'admin/config/detail_view.html'

        cxt = {

           'data' : config,

        }        

        return render_to_response(config_detail_view_template , cxt, context_instance=RequestContext(request))

        

    def action(self,form):

         return "<a href='view/%s'>view</a>" % (form.id)

    action.allow_tags = True


 

admin.site.register(Config, ConfigAdmin)