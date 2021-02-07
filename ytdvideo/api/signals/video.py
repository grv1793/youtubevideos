def video_post_save_signal(instance, created):
    from api.helpers.elasticmodelhelpers.videoelasticmodelhelper import VideoElasticModelHelper
    if created:
        print("created")
        VideoElasticModelHelper().push_obj_to_es(instance)
    else:
        print("updated")
        VideoElasticModelHelper().update_model_es_data(instance)
