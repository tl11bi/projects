package sample_file_provider

import (
	"context"

	"github.com/hashicorp/terraform-plugin-sdk/v2/diag"
	"github.com/hashicorp/terraform-plugin-sdk/v2/helper/schema"
)

func resourceFile() *schema.Resource {
	return &schema.Resource{
		Description: "A file.",

		CreateContext: resourceFileCreate,
		ReadContext:   resourceFileRead,
		UpdateContext: resourceFileCreate, // In our case Update == Create
		DeleteContext: resourceFileDelete,

		Schema: map[string]*schema.Schema{
			"file_content": {
				Description: "What goes in the file",
				Type:        schema.TypeString,
				Optional:    true,
			},
			"filename": {
				Description: "The file to manage",
				Type:        schema.TypeString,
				Required:    true,
			},
		},
	}
}

func dataSourceFile() *schema.Resource {
	return &schema.Resource{
		Description: "A file.",

		// Normally our data source would be defined elsewhere, but it's literally
		// identical to a resource read for this running-example.
		ReadContext: resourceFileRead,

		Schema: map[string]*schema.Schema{
			"file_content": {
				Description: "The contents we read from the file",
				Computed:    true,
				Type:        schema.TypeString,
				Elem: &schema.Schema{
					Type:     schema.TypeString,
					Computed: true,
				},
			},
			"filename": {
				Description: "The file to read",
				Type:        schema.TypeString,
				Required:    true,
			},
		},
	}
}

func resourceFileCreate(ctx context.Context, d *schema.ResourceData, meta interface{}) diag.Diagnostics {
	var err error
	if content, ok := d.GetOk("file_content"); ok {
		err = meta.(*fileClient).write(d.Get("filename").(string), content.(string))
	} else {
		err = meta.(*fileClient).write(d.Get("filename").(string), "")
	}
	if err != nil {
		return diag.FromErr(err)
	}
	d.SetId(d.Get("filename").(string))

	return nil
}

func resourceFileRead(ctx context.Context, d *schema.ResourceData, meta interface{}) diag.Diagnostics {
	content, err := meta.(*fileClient).read(d.Get("filename").(string))
	if err != nil {
		return diag.FromErr(err)
	}

	d.Set("file_content", content)
	d.SetId(d.Get("filename").(string))

	return nil
}

func resourceFileDelete(ctx context.Context, d *schema.ResourceData, meta interface{}) diag.Diagnostics {
	err := meta.(*fileClient).delete(d.Get("filename").(string))
	if err != nil {
		return diag.FromErr(err)
	}
	return nil
}
