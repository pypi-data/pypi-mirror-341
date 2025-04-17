
from kotonebot.tasks.common import sprite_path
from kotonebot.backend.core import Image, HintBox, HintPoint



class Common:
    
    ButtonClose = Image(path=sprite_path(r"0b60edc5-f60f-4f78-b3d1-a03855160371.png"), name="button_close.png")

    ButtonCompletion = Image(path=sprite_path(r"3243c677-004c-43d0-82c0-c702ef4c9bfc.png"), name="button_completion.png")

    ButtonConfirm = Image(path=sprite_path(r"188af1b6-2b57-4ff5-be6a-0e5fa2cd9311.png"), name="button_confirm.png")

    ButtonConfirmNoIcon = Image(path=sprite_path(r"566c560a-8b5e-4904-baac-cfa1135d7920.png"), name="button_confirm_no_icon.png")

    ButtonContest = Image(path=sprite_path(r"47b6d351-1260-4a38-8112-37f55cdcc9f0.png"), name="button_contest.png")

    ButtonEnd = Image(path=sprite_path(r"1900de8d-610f-4d85-b6a1-eae1df0aa8f5.png"), name="button_end.png")

    ButtonHome = Image(path=sprite_path(r"31966f9b-502b-4d31-92be-add93aa54d98.png"), name="button_home.png")

    ButtonIconArrowShort = Image(path=sprite_path(r"fa862c24-0bda-485e-8530-0cc3a519ed65.png"), name="button_icon_arrow_short.png")

    ButtonIconArrowShortDisabled = Image(path=sprite_path(r"02e054d5-abab-410b-9978-3a7c087ca3cf.png"), name="button_icon_arrow_short_disabled.png")

    ButtonIconCheckMark = Image(path=sprite_path(r"506c4a6b-f0e4-47a8-b4d4-5ff7855c81a4.png"), name="button_icon_check_mark.png")

    ButtonIconClose = Image(path=sprite_path(r"8f546d8b-9d18-4bd3-b912-5a5163ea4972.png"), name="button_icon_close.png")

    ButtonIdol = Image(path=sprite_path(r"18e78865-784d-433e-abdb-bc28ac3a4c2b.png"), name="button_idol.png")

    ButtonIdolSupportCard = Image(path=sprite_path(r"a0262fc2-3627-4eea-aa54-4a6ae1c26b1b.png"), name="button_idol_support_card.png")

    ButtonNext = Image(path=sprite_path(r"2c76ab0b-0f57-4e41-87c8-21ca0603fce6.png"), name="button_next.png")

    ButtonNextNoIcon = Image(path=sprite_path(r"b3aa25a8-ab50-4e73-aafe-8822ca73e2d0.png"), name="button_next_no_icon.png")

    ButtonRetry = Image(path=sprite_path(r"ad3d3d9e-df7a-499a-94e8-aa4da2ef1f83.png"), name="button_retry.png")

    ButtonSelect = Image(path=sprite_path(r"df17b9d4-97fd-4146-8bd9-e81d190cdccb.png"), name="button_select.png")

    ButtonStart = Image(path=sprite_path(r"357d81f0-8021-4255-a9e8-4ab545bab62c.png"), name="button_start.png")

    ButtonToolbarHome = Image(path=sprite_path(r"4e84766d-69ef-4e6a-99cd-24879ee44676.png"), name="button_toolbar_home.png")

    ButtonToolbarMenu = Image(path=sprite_path(r"e03a1d1c-ac64-43d9-9701-99531ebf364c.png"), name="button_toolbar_menu.png")

    CheckboxUnchecked = Image(path=sprite_path(r"7791ad05-78c1-4254-bdd0-e8a67f5542be.png"), name="checkbox_unchecked.png")

    TextGameUpdate = Image(path=sprite_path(r"1c7b4e4f-6a34-47c0-8ed5-1009ee804944.png"), name="text_game_update.png")

    TextNetworkError = Image(path=sprite_path(r"cbb4f73b-b7e5-4e5a-92fe-d5126bf6ab73.png"), name="text_network_error.png")

    TextFastforwardCommuDialogTitle = Image(path=sprite_path(r"50e23c8a-7ba2-4c9c-9cfb-196c260fa1d5.png"), name="早送り確認")

    ButtonCommuSkip = Image(path=sprite_path(r"f1f21925-3e22-4dd1-b53b-bb52bcf26c2b.png"), name="跳过交流按钮")

    ButtonCommuFastforward = Image(path=sprite_path(r"f6ca6bd3-543f-4779-8367-c5c883f04b95.png"), name="快进交流按钮")

    ButtonOK = Image(path=sprite_path(r"8424ecdd-8857-4764-9fd0-d4bfa440c128.png"), name="OK 按钮")

    ButtonSelect2 = Image(path=sprite_path(r"5ebcde3b-f0fd-4e5d-b3de-ada8f0b5e03b.png"), name="選択する")

    TextSkipCommuComfirmation = Image(path=sprite_path(r"4d78add6-1027-4939-bb51-f99fca7db2ce.png"), name="跳过未读交流确认对话框标题")

    IconButtonCheck = Image(path=sprite_path(r"fad5eec2-5fd5-412f-9abb-987a3087dc54.png"), name="按钮✓图标")

    IconButtonCross = Image(path=sprite_path(r"bc7155ac-18c9-4335-9ec2-c8762d37a057.png"), name="按钮×图标")


    pass
class Daily:
    
    ButonLinkData = Image(path=sprite_path(r"a15638f0-0ce2-47c6-be7e-e478fc08b670.png"), name="buton_link_data.png")

    ButtonAssignmentPartial = Image(path=sprite_path(r"bf6abcb1-5535-4caf-8c4c-0c08e96b207d.png"), name="button_assignment_partial.png")

    ButtonClaimAllNoIcon = Image(path=sprite_path(r"57868439-ce99-4551-a539-15804fbebac5.png"), name="button_claim_all_no_icon.png")

    ButtonClubCollectReward = Image(path=sprite_path(r"149431c2-e459-4366-876b-5c9609b08145.png"), name="button_club_collect_reward.png")

    ButtonClubSendGift = Image(path=sprite_path(r"b268aa27-ba54-47cd-ba98-2bcc2974c562.png"), name="button_club_send_gift.png")

    ButtonClubSendGiftNext = Image(path=sprite_path(r"b862e805-bd62-4a11-964f-c5e99d41d87a.png"), name="button_club_send_gift_next.png")

    ButtonContestChallenge = Image(path=sprite_path(r"8d489e63-736e-4a61-8fc2-41cf013e8e68.png"), name="button_contest_challenge.png")

    ButtonContestChallengeStart = Image(path=sprite_path(r"350ed1fb-144c-4078-b829-54596c981be2.png"), name="button_contest_challenge_start.png")

    ButtonContestRanking = Image(path=sprite_path(r"aef91360-2d5b-4cc2-a727-932e5f5fa8fe.png"), name="button_contest_ranking.png")

    ButtonContestStart = Image(path=sprite_path(r"3c65dec3-c63a-4b2c-ae8c-67b6089dd398.png"), name="button_contest_start.png")

    ButtonDailyShop = Image(path=sprite_path(r"dfea6258-b349-4849-979a-6fe33b7478b2.png"), name="button_daily_shop.png")

    ButtonHomeCurrent = Image(path=sprite_path(r"b8c6c0d8-280f-43eb-b1ed-b834509ddf31.png"), name="button_home_current.png")

    ButtonIconPass = Image(path=sprite_path(r"82a4f817-4b9f-44a0-b127-e329d17f2fc4.png"), name="button_icon_pass.png")

    ButtonIconSkip = Image(path=sprite_path(r"15d68b47-8682-4ff5-ae6f-0582e1f3da99.png"), name="button_icon_skip.png")

    ButtonMission = Image(path=sprite_path(r"e4f3ca42-0754-419c-a901-2b375c61413f.png"), name="button_mission.png")

    ButtonPass = Image(path=sprite_path(r"af3846f2-9226-4f35-8d2c-5e6dbea6ae5b.png"), name="button_pass.png")

    ButtonPassClaim = Image(path=sprite_path(r"e7c0576c-cb5b-47f2-8085-36610e29f39c.png"), name="button_pass_claim.png")

    ButtonPresentsPartial = Image(path=sprite_path(r"a4289c3d-c286-46e7-a7aa-e0732d3ca025.png"), name="button_presents_partial.png")

    ButtonProduce = Image(path=sprite_path(r"fd1ecad1-324e-406d-8087-02f04026de88.png"), name="button_produce.png")

    ButtonShop = Image(path=sprite_path(r"ce7d667d-81e0-4405-9581-00ff73252332.png"), name="button_shop.png")

    ButtonShopCapsuleToys = Image(path=sprite_path(r"137e9e84-b261-44b3-b242-fce04565442a.png"), name="button_shop_capsule_toys.png")

    ButtonShopCapsuleToysDraw = Image(path=sprite_path(r"db95b204-9da7-45fe-8fa3-f23d5014f99c.png"), name="button_shop_capsule_toys_draw.png")

    ButtonShopCountAdd = Image(path=sprite_path(r"3b8a3590-1fc3-4d02-9499-3ef30b629d15.png"), name="button_shop_count_add.png")

    ButtonShopCountAddDisabled = Image(path=sprite_path(r"dbfcf81a-688a-40cd-b14b-b1cbd8029ef5.png"), name="button_shop_count_add_disabled.png")

    ButtonSupportCardUpgrade = Image(path=sprite_path(r"d7ea6f44-fad0-4354-8749-c199e75368c4.png"), name="button_support_card_upgrade.png")

    IconTitleDailyShop = Image(path=sprite_path(r"e9ee330d-dfca-440e-8b8c-0a3b4e8c8730.png"), name="日常商店标题图标")

    BoxHomeAssignment = HintBox(x1=16, y1=642, x2=127, y2=752, source_resolution=(720, 1280))

    BoxHomeAP = HintBox(x1=291, y1=4, x2=500, y2=82, source_resolution=(720, 1280))

    BoxHomeJewel = HintBox(x1=500, y1=7, x2=703, y2=82, source_resolution=(720, 1280))

    BoxHomeActivelyFunds = HintBox(x1=11, y1=517, x2=137, y2=637, source_resolution=(720, 1280))

    IconAssignKouchou = Image(path=sprite_path(r"c46f9f81-739f-4b00-bae4-5caff7901a0a.png"), name="icon_assign_kouchou.png")

    IconAssignMiniLive = Image(path=sprite_path(r"39e8c36f-2ca2-46c1-b867-6b15d8da1827.png"), name="icon_assign_mini_live.png")

    IconAssignOnlineLive = Image(path=sprite_path(r"bad71a65-f831-4f94-a68e-dc548c3faffc.png"), name="icon_assign_online_live.png")

    IconAssignTitle = Image(path=sprite_path(r"5a3fd66f-656a-41eb-85d6-0a2d19b26484.png"), name="icon_assign_title.png")

    IconMenuClub = Image(path=sprite_path(r"4b10692f-dfbe-4d2a-88b8-4572b77d04fc.png"), name="icon_menu_club.png")

    IconShopAp = Image(path=sprite_path(r"afca7821-0fca-4eb9-a386-49d8e678b80c.png"), name="icon_shop_ap.png")

    IconShopMoney = Image(path=sprite_path(r"8b824805-e7df-479f-be2f-8da7840c6758.png"), name="icon_shop_money.png")

    IconShopTitle = Image(path=sprite_path(r"b5aa9c09-8c60-4325-b0eb-fe183ee63f53.png"), name="icon_shop_title.png")

    IconTitleAssign = Image(path=sprite_path(r"b2711d53-3a34-4087-8690-efca3d437d12.png"), name="icon_title_assign.png")

    IconTitlePass = Image(path=sprite_path(r"6c5a22ec-8db3-4a84-8bd9-c8effada8a8d.png"), name="icon_title_pass.png")

    BoxApkUpdateDialogTitle = HintBox(x1=26, y1=905, x2=342, y2=967, source_resolution=(720, 1280))

    ButtonAssignmentShortenTime = Image(path=sprite_path(r"1652f06a-5417-49ef-8949-4854772d9ab7.png"), name="工作页面 短缩 时间")

    class Club:
        
        NoteRequestHintBox = HintBox(x1=314, y1=1071, x2=450, y2=1099, source_resolution=(720, 1280))
    
    
        pass
    PointDissmissContestReward = HintPoint(x=604, y=178)

    BoxMissonTabs = HintBox(x1=11, y1=929, x2=703, y2=1030, source_resolution=(720, 1280))

    class CapsuleToys:
        
        NextPageStartPoint = HintPoint(x=360, y=1167)
    
        NextPageEndPoint = HintPoint(x=362, y=267)
    
        IconTitle = Image(path=sprite_path(r"2bd6fe88-99fa-443d-8e42-bb3de5881213.png"), name="日常 扭蛋 页面标题图标")
    
        SliderStartPoint = HintPoint(x=476, y=898)
    
        SliderEndPoint = HintPoint(x=230, y=898)
    
    
        pass
    TextDefaultExchangeCountChangeDialog = Image(path=sprite_path(r"de325534-3fd3-480a-9eb8-eb47960a753a.png"), name="商店默认购买次数改变对话框")

    class SupportCard:
        
        DragDownStartPoint = HintPoint(x=357, y=872)
    
        DragDownEndPoint = HintPoint(x=362, y=194)
    
        TargetSupportCard = HintPoint(x=138, y=432)
    
    
        pass
    TextActivityFundsMax = Image(path=sprite_path(r"ef75bc45-b7b5-4c1d-a92f-eb792081a800.png"), name="text_activity_funds_max.png")

    TextAssignmentCompleted = Image(path=sprite_path(r"def4deed-c3d3-4300-83b2-0e62757e4d73.png"), name="text_assignment_completed.png")

    TextContest = Image(path=sprite_path(r"c67da0db-894e-416b-b086-50826f620ad3.png"), name="text_contest.png")

    TextContestLastOngoing = Image(path=sprite_path(r"0f41d858-5132-469f-8aa7-281e9ea28004.png"), name="text_contest_last_ongoing.png")

    TextContestNoMemory = Image(path=sprite_path(r"0b48747c-3d2c-4bab-9088-170bd219ea76.png"), name="text_contest_no_memory.png")

    TextContestOverallStats = Image(path=sprite_path(r"0e8508dc-9228-42b7-b160-c2a2851a0013.png"), name="text_contest_overall_stats.png")

    TextShopPurchased = Image(path=sprite_path(r"90d2bbe7-2dbd-4b6e-a049-faaf123bc16a.png"), name="text_shop_purchased.png")

    TextShopRecommended = Image(path=sprite_path(r"00c3d3e5-0129-4de1-b8d9-ff617dcdd9d2.png"), name="text_shop_recommended.png")

    TextTabShopAp = Image(path=sprite_path(r"87c7a669-a55f-4af5-9366-af7cc530b648.png"), name="text_tab_shop_ap.png")


    pass
class Shop:
    
    ItemLessonNote = Image(path=sprite_path(r"0949c622-9067-4f0d-bac2-3f938a1d2ed2.png"), name="レッスンノート")

    ItemVeteranNote = Image(path=sprite_path(r"b2af59e9-60e3-4d97-8c72-c7ba092113a3.png"), name="ベテランノート")

    ItemSupportEnhancementPt = Image(path=sprite_path(r"835489e2-b29b-426c-b4c9-3bb9f8eb6195.png"), name="サポート強化Pt 支援强化Pt")

    ItemSenseNoteVocal = Image(path=sprite_path(r"c5b7d67e-7260-4f08-a0e9-4d31ce9bbecf.png"), name="センスノート（ボーカル）感性笔记（声乐）")

    ItemSenseNoteDance = Image(path=sprite_path(r"0f7d581d-cea3-4039-9205-732e4cd29293.png"), name="センスノート（ダンス）感性笔记（舞蹈）")

    ItemSenseNoteVisual = Image(path=sprite_path(r"d3cc3323-51af-4882-ae12-49e7384b746d.png"), name="センスノート（ビジュアル）感性笔记（形象）")

    ItemLogicNoteVocal = Image(path=sprite_path(r"a1df3af1-a3e7-4521-a085-e4dc3cd1cc57.png"), name="ロジックノート（ボーカル）理性笔记（声乐）")

    ItemLogicNoteDance = Image(path=sprite_path(r"a9fcaf04-0c1f-4b0f-bb5b-ede9da96180f.png"), name="ロジックノート（ダンス）理性笔记（舞蹈）")

    ItemLogicNoteVisual = Image(path=sprite_path(r"c3f536d6-a04a-4651-b3f9-dd2c22593f7f.png"), name="ロジックノート（ビジュアル）理性笔记（形象）")

    ItemAnomalyNoteVocal = Image(path=sprite_path(r"eef25cf9-afd0-43b1-b9c5-fbd997bd5fe0.png"), name="アノマリーノート（ボーカル）非凡笔记（声乐）")

    ItemAnomalyNoteDance = Image(path=sprite_path(r"df991b42-ed8e-4f2c-bf0c-aa7522f147b6.png"), name="アノマリーノート（ダンス）非凡笔记（舞蹈）")

    ItemAnomalyNoteVisual = Image(path=sprite_path(r"9340b854-025c-40da-9387-385d38433bef.png"), name="アノマリーノート（ビジュアル）非凡笔记（形象）")

    ItemRechallengeTicket = Image(path=sprite_path(r"ea1ba124-9cb3-4427-969a-bacd47e7d920.png"), name="再挑戦チケット 重新挑战券")

    ItemRecordKey = Image(path=sprite_path(r"1926f2f9-4bd7-48eb-9eba-28ec4efb0606.png"), name="記録の鍵  解锁交流的物品")

    class IdolPiece:
        
        倉本千奈_WonderScale = Image(path=sprite_path(r"6720b6e8-ae80-4cc0-a885-518efe12b707.png"), name="倉本千奈 WonderScale 碎片")
    
        篠泽广_光景 = Image(path=sprite_path(r"afa06fdc-a345-4384-b25d-b16540830256.png"), name="篠泽广 光景 碎片")
    
        紫云清夏_TameLieOneStep = Image(path=sprite_path(r"278b7d9c-707e-4392-9677-74574b5cdf42.png"), name="紫云清夏 Tame-Lie-One-Step 碎片")
    
        葛城リーリヤ_白線 = Image(path=sprite_path(r"74ff07b3-d91c-4579-80cd-379ed7020622.png"), name="葛城リーリヤ 白線 碎片")
    
        姫崎薪波_cIclumsy_trick  = Image(path=sprite_path(r"a7f5abf1-982f-4a55-8d41-3ad6f56798e0.png"), name="姫崎薪波 cIclumsy trick 碎片")
    
        花海咲季_FightingMyWay = Image(path=sprite_path(r"2bc00520-0afe-40e5-8743-d33fc6b2945a.png"), name="花海咲季 FightingMyWay 碎片")
    
        藤田ことね_世界一可愛い私 = Image(path=sprite_path(r"135ee57a-d30d-4ba8-83f0-9f1681a49ff7.png"), name="藤田ことね 世界一可愛い私 碎片")
    
        花海佑芽_TheRollingRiceball = Image(path=sprite_path(r"d15959bf-d07b-4f07-948a-c0aeaf17756a.png"), name="花海佑芽 The Rolling Riceball 碎片")
    
        月村手毬_LunaSayMaybe = Image(path=sprite_path(r"868b97a9-492e-4712-b47f-82b97495b019.png"), name="月村手毬 Luna say maybe 碎片")
    
    
        pass

    pass
class Produce:
    
    BoxProduceOngoing = HintBox(x1=179, y1=937, x2=551, y2=1091, source_resolution=(720, 1280))

    ButtonAutoSet = Image(path=sprite_path(r"0961d712-2dae-4348-ad5f-b1527e931c92.png"), name="button_auto_set.png")

    ButtonProduce = Image(path=sprite_path(r"b0e9244a-c338-46bf-a160-dc229c848d52.png"), name="button_produce.png")

    ButtonProduceStart = Image(path=sprite_path(r"475b6b80-25c3-45f4-a5d2-343e3137b2d6.png"), name="button_produce_start.png")

    ButtonRegular = Image(path=sprite_path(r"47de813c-3d73-4bb1-9731-b80f721590b4.png"), name="button_regular.png")

    CheckboxIconNoteBoost = Image(path=sprite_path(r"7b70838d-74b4-4500-a10d-ff7fa996435f.png"), name="checkbox_icon_note_boost.png")

    CheckboxIconSupportPtBoost = Image(path=sprite_path(r"178ce25a-f12c-49a0-b5ed-69b9bcec338c.png"), name="checkbox_icon_support_pt_boost.png")

    IconPIdolLevel = Image(path=sprite_path(r"30a6f399-6999-4f04-bb77-651e0214112f.png"), name="P偶像卡上的等级图标")

    KbIdolOverviewName = HintBox(x1=140, y1=16, x2=615, y2=97, source_resolution=(720, 1280))

    BoxIdolOverviewIdols = HintBox(x1=26, y1=568, x2=696, y2=992, source_resolution=(720, 1280))

    ButtonResume = Image(path=sprite_path(r"ccbcb114-7f73-43d1-904a-3a7ae660c531.png"), name="再開する")

    ResumeDialogRegular = Image(path=sprite_path(r"daf3d823-b7f1-4584-acf3-90b9d880332c.png"), name="培育再开对话框 REGULAR")

    BoxResumeDialogWeeks = HintBox(x1=504, y1=559, x2=643, y2=595, source_resolution=(720, 1280))

    BoxResumeDialogIdolCard = HintBox(x1=53, y1=857, x2=197, y2=1048, source_resolution=(720, 1280))

    ResumeDialogPro = Image(path=sprite_path(r"c954e153-d3e9-4488-869f-d00cfdfac5ee.png"), name="培育再开对话框 PRO")

    RadioTextSkipCommu = Image(path=sprite_path(r"26d38945-c466-45dd-b29a-0580d86df2d4.png"), name="radio_text_skip_commu.png")

    TextAnotherIdolAvailableDialog = Image(path=sprite_path(r"cbf4ce9c-f8d8-4fb7-a197-15bb9847df04.png"), name="Another 版本偶像可用对话框标题")

    TextAPInsufficient = Image(path=sprite_path(r"4883c564-f950-4a29-9f5f-6f924123cd22.png"), name="培育 AP 不足提示弹窗 标题")

    ButtonRefillAP = Image(path=sprite_path(r"eaba6ebe-f0df-4918-aee5-ef4e3ffedcf0.png"), name="确认恢复AP按钮")

    ButtonUse = Image(path=sprite_path(r"cfc9c8e8-cbe1-49f0-9afa-ead7f9455a2e.png"), name="按钮「使う」")

    ScreenshotNoEnoughAp3 = Image(path=sprite_path(r"0a88b225-1b32-4635-8b5c-c66eb77d54ee.png"), name="screenshot_no_enough_ap_3.png")

    ButtonSkipLive = Image(path=sprite_path(r"e5e84f9e-28da-4cf4-bcba-c9145fe39b07.png"), name="培育结束跳过演出按钮")

    TextSkipLiveDialogTitle = Image(path=sprite_path(r"b6b94f21-ef4b-4425-9c7e-ca2b574b0add.png"), name="跳过演出确认对话框标题")

    BoxModeButtons = HintBox(x1=7, y1=818, x2=713, y2=996, source_resolution=(720, 1280))

    ButtonPIdolOverview = Image(path=sprite_path(r"e88c9ad1-ec37-4fcd-b086-862e1e7ce8fd.png"), name="Pアイドルー覧  P偶像列表展示")

    TextStepIndicator1 = Image(path=sprite_path(r"44ba8515-4a60-42c9-8878-b42e4e34ee15.png"), name="1. アイドル選択")

    BoxSetCountIndicator = HintBox(x1=17, y1=671, x2=119, y2=707, source_resolution=(720, 1280))

    PointProduceNextSet = HintPoint(x=702, y=832)

    PointProducePrevSet = HintPoint(x=14, y=832)

    TextStepIndicator2 = Image(path=sprite_path(r"a48324ae-7c1a-489e-b3c4-93d12267f88d.png"), name="2. サポート選択")

    TextStepIndicator3 = Image(path=sprite_path(r"f43c313b-8a7b-467b-8442-fc5bcb8b4388.png"), name="3.メモリー選択")

    TextStepIndicator4 = Image(path=sprite_path(r"b62bf889-da3c-495a-8707-f3bde73efe92.png"), name="4.開始確認")

    TextRentAvailable = Image(path=sprite_path(r"a980dd93-d57e-4258-b9d1-26ea8e8301d2.png"), name="text_rent_available.png")


    pass
class InPurodyuusu:
    
    A = Image(path=sprite_path(r"2cb70cda-6dd9-48d1-8472-1431ae4b3812.png"), name="A.png")

    AcquireBtnDisabled = Image(path=sprite_path(r"ec819f63-628c-405a-bcb4-27b5ad7aa67c.png"), name="acquire_btn_disabled.png")

    ButtonCancel = Image(path=sprite_path(r"60adc923-f8d0-40f6-a869-6715a3167b77.png"), name="button_cancel.png")

    ButtonComplete = Image(path=sprite_path(r"5c05a156-5f5e-4896-a082-42584d973399.png"), name="button_complete.png")

    ButtonFinalPracticeDance = Image(path=sprite_path(r"7a4b5199-971d-4f05-b910-7a28178af952.png"), name="button_final_practice_dance.png")

    ButtonFinalPracticeVisual = Image(path=sprite_path(r"72fd247b-5af0-42c4-91b0-c40afe9fc675.png"), name="button_final_practice_visual.png")

    ButtonFinalPracticeVocal = Image(path=sprite_path(r"e0beb7eb-d62e-463e-98db-4d14801ca678.png"), name="button_final_practice_vocal.png")

    ButtonFollowNoIcon = Image(path=sprite_path(r"55953b78-ad43-46e8-b826-056b45df5e40.png"), name="button_follow_no_icon.png")

    ButtonIconStudy = Image(path=sprite_path(r"f4a9a5ee-ec7e-4778-b901-422ff5949ab8.png"), name="button_icon_study.png")

    ButtonIconStudyVisual = Image(path=sprite_path(r"f5394b14-cf8b-46a7-9fea-0db0a3a2e699.png"), name="button_icon_study_visual.png")

    ButtonLeave = Image(path=sprite_path(r"03e89b12-1cb9-4ca6-a2f2-0edcc29bdadc.png"), name="button_leave.png")

    ButtonNextNoIcon = Image(path=sprite_path(r"2cd87c29-5967-455a-b0dd-561d6e0b8d37.png"), name="button_next_no_icon.png")

    ButtonRetry = Image(path=sprite_path(r"77e0a4ef-a161-40a5-b161-ec4410a5a1a9.png"), name="button_retry.png")

    ButtonTextActionOuting = Image(path=sprite_path(r"34b2258f-833c-419e-b37e-4338674fd365.png"), name="button_text_action_outing.png")

    ButtonTextAllowance = Image(path=sprite_path(r"2048c09a-46e7-472d-9831-2f4367be10bf.png"), name="button_text_allowance.png")

    ButtonTextConsult = Image(path=sprite_path(r"0a1d35f7-ca2e-4cfd-98f9-b4b687160983.png"), name="button_text_consult.png")

    IconClearBlue = Image(path=sprite_path(r"9c031b89-f2ad-4fd8-8ae5-5b0c74fbd3ab.png"), name="icon_clear_blue.png")

    IconTitleAllowance = Image(path=sprite_path(r"0fd35cec-9880-42be-b868-a8c4ee1efa37.png"), name="icon_title_allowance.png")

    IconTitleStudy = Image(path=sprite_path(r"fed22f37-336a-4cec-99cd-e4d22231c080.png"), name="icon_title_study.png")

    LootboxSliverLock = Image(path=sprite_path(r"32defbb8-c295-4781-9a92-90e423e8849e.png"), name="lootbox_sliver_lock.png")

    LootBoxSkillCard = Image(path=sprite_path(r"a4fd3565-d389-4c42-948b-dde4b1e0d047.png"), name="loot_box_skill_card.png")

    M = Image(path=sprite_path(r"aab790a5-e5ca-427b-bee1-4fee5fba2578.png"), name="M.png")

    BoxWeeksUntilExam = HintBox(x1=11, y1=8, x2=237, y2=196, source_resolution=(720, 1280))

    TextActionVocal = Image(path=sprite_path(r"d6b64759-26b7-45b1-bf8e-5c0d98611e0d.png"), name="Vo. レッスン")

    TextActionDance = Image(path=sprite_path(r"303cccc1-c674-4d3a-8c89-19ea729fdbef.png"), name="Da. レッスン")

    TextActionVisual = Image(path=sprite_path(r"cc8a495d-330d-447d-8a80-a8a6ecc409c5.png"), name="Vi. レッスン")

    IconAsariSenseiAvatar = Image(path=sprite_path(r"d7667903-7149-4f2f-9c15-d8a4b5f4d347.png"), name="Asari 老师头像")

    BoxAsariSenseiTip = HintBox(x1=245, y1=150, x2=702, y2=243, source_resolution=(720, 1280))

    ButtonPracticeVocal = Image(path=sprite_path(r"ce1d1d6f-38f2-48bf-98bd-6e091c7ca5b8.png"), name="行动页 声乐课程按钮图标")

    ButtonPracticeDance = Image(path=sprite_path(r"b2e1bf3c-2c36-4fb5-9db7-c10a29563a37.png"), name="行动页 舞蹈课程按钮图标")

    ButtonPracticeVisual = Image(path=sprite_path(r"adc533a7-970b-4c5b-a037-2181531a35d6.png"), name="行动页 形象课程按钮图标")

    BoxExamTop = HintBox(x1=5, y1=2, x2=712, y2=55, source_resolution=(720, 1280))

    BoxCardLetter = HintBox(x1=6, y1=1081, x2=715, y2=1100, source_resolution=(720, 1280))

    PDrinkIcon = Image(path=sprite_path(r"678425ad-b9c8-4c95-b986-dee0f0e01174.png"), name="p_drink_icon.png")

    PItemIconColorful = Image(path=sprite_path(r"99cf33fc-0da8-43d3-9537-388295f2b22c.png"), name="p_item_icon_colorful.png")

    PSkillCardIconBlue = Image(path=sprite_path(r"8c6b1ceb-c8e9-41f0-b518-041e9d441d0c.png"), name="p_skill_card_icon_blue.png")

    PSkillCardIconColorful = Image(path=sprite_path(r"79b545ce-d3cb-4bc9-a8a1-44cc5202cea4.png"), name="p_skill_card_icon_colorful.png")

    Rest = Image(path=sprite_path(r"4980e938-7b71-4978-add9-b6541b3d5980.png"), name="rest.png")

    RestConfirmBtn = Image(path=sprite_path(r"7120e799-961f-44a5-a96f-42942d549f6e.png"), name="rest_confirm_btn.png")

    Screenshot4Cards = Image(path=sprite_path(r"cd3a4750-31aa-4be4-9860-4c914b5565d7.png"), name="screenshot_4_cards.png")

    Screenshot5Cards = Image(path=sprite_path(r"daa17a2f-6315-4d65-bfa7-7622d3e6156e.png"), name="screenshot_5_cards.png")

    ButtonIconOuting = Image(path=sprite_path(r"8ded6c98-85ea-4858-a66d-4fc8caecb7c5.png"), name="行动按钮图标 外出（おでかけ）")

    TextGoalClearNext = Image(path=sprite_path(r"05890a1b-8764-4e9f-9d21-65d292c22e13.png"), name="培育目标达成 NEXT 文字")

    BoxLessonCards5_1 = HintBox(x1=16, y1=882, x2=208, y2=1136, source_resolution=(720, 1280))

    BoxNoSkillCard = HintBox(x1=180, y1=977, x2=529, y2=1026, source_resolution=(720, 1280))

    TitleIconOuting = Image(path=sprite_path(r"ee4e512b-4982-49b6-9c71-31984b58e1d0.png"), name="外出（おでかけ）页面 标题图标")

    TextPDrinkMaxConfirmTitle = Image(path=sprite_path(r"582d36c0-0916-4706-9833-4fbc026701f5.png"), name="P饮料溢出 不领取弹窗标题")

    IconTitleSkillCardRemoval = Image(path=sprite_path(r"bab6c393-692c-4681-ac0d-76c0d9dabea6.png"), name="技能卡自选删除 标题图标")

    ButtonRemove = Image(path=sprite_path(r"00551158-fee9-483f-b034-549139a96f58.png"), name="削除")

    TextPDrink = Image(path=sprite_path(r"8c179a21-be6f-4db8-a9b0-9afeb5c36b1c.png"), name="文本「Pドリンク」")

    TextDontClaim = Image(path=sprite_path(r"e4683def-8d1d-472b-a5ab-bb3885c0c98e.png"), name="受け取らない")

    ButtonDontClaim = Image(path=sprite_path(r"447d0e44-5d87-4b7c-8e60-edb111fe1639.png"), name="「受け取らない」按钮")

    BoxSelectPStuffComfirm = HintBox(x1=256, y1=1064, x2=478, y2=1128, source_resolution=(720, 1280))

    TextClaim = Image(path=sprite_path(r"c948f136-416f-447e-8152-54a1cd1d1329.png"), name="文字「受け取る」")

    TextPItem = Image(path=sprite_path(r"0c0627be-4a09-4450-a078-1858d3ace532.png"), name="文字「Pアイテム」")

    TextSkillCard = Image(path=sprite_path(r"d271a24f-efe8-424d-8fd5-f6b3756ba4ca.png"), name="文字「スキルカード」")

    BoxSkillCardAcquired = HintBox(x1=194, y1=712, x2=528, y2=765, source_resolution=(720, 1280))

    IconSkillCardEventBubble = Image(path=sprite_path(r"6b58d90d-2e5e-4b7f-bc01-941f2633de89.png"), name="技能卡事件气泡框图标")

    ScreenshotSkillCardEnhanceDialog = Image(path=sprite_path(r"ae19b960-7a70-4cab-9efc-84cc558de03d.png"), name="screenshot_skill_card_enhance_dialog.png")

    IconTitleSkillCardEnhance = Image(path=sprite_path(r"79abd239-5eed-4195-9fa8-d729daa874ca.png"), name="技能卡强化 标题 图标")

    ButtonEnhance = Image(path=sprite_path(r"da439e8c-3b74-4371-9657-0736d826c7d1.png"), name="技能卡 强化按钮")

    IconTitleSkillCardMove = Image(path=sprite_path(r"db7d3f03-1f7f-43bf-8125-f7c2d345fca2.png"), name="培育中技能卡移动对话框")

    BoxSkillCardMoveButtonCount = HintBox(x1=339, y1=1170, x2=381, y2=1195, source_resolution=(720, 1280))

    T = Image(path=sprite_path(r"16fbc93d-b294-4001-b4e9-ee2af181415f.png"), name="睡意卡字母 T（眠気）")

    IconSp = Image(path=sprite_path(r"d982d2b5-4bc0-4ae9-a516-f29c2848d64b.png"), name="SP 课程图标")

    BoxCommuEventButtonsArea = HintBox(x1=14, y1=412, x2=703, y2=1089, source_resolution=(720, 1280))

    TextSelfStudyVocal = Image(path=sprite_path(r"c78c38cc-7b61-4dc4-820d-0a5b684ef52e.png"), name="文化课事件 自习 声乐")

    TextSelfStudyDance = Image(path=sprite_path(r"83d0a033-466c-463a-bb8c-be0f2953e9b2.png"), name="文化课事件 自习 舞蹈")

    TextSelfStudyVisual = Image(path=sprite_path(r"4695f96b-c4f5-4bb6-a021-a13b6ceb2883.png"), name="文化课事件 自习 形象")

    TextAsariProduceEnd = Image(path=sprite_path(r"b621638c-c7ff-44b8-b8ce-8384d683bf5b.png"), name="text_asari_produce_end.png")

    TextButtonExamSkipTurn = Image(path=sprite_path(r"f653fc36-8589-4c88-b2bf-eae1e3733548.png"), name="text_button_exam_skip_turn.png")

    TextClearUntil = Image(path=sprite_path(r"b8b9ad1c-837d-445d-94b7-b6922c31e1ba.png"), name="text_clear_until.png")

    TextDance = Image(path=sprite_path(r"386c4f7a-4ccf-439b-b28a-93d5053ef246.png"), name="text_dance.png")

    TextFinalProduceRating = Image(path=sprite_path(r"7eed6182-7e21-447e-9471-18f31524988c.png"), name="text_final_produce_rating.png")

    TextOneWeekRemaining = Image(path=sprite_path(r"60565d55-bed0-4646-a66a-5b67180f0d32.png"), name="text_one_week_remaining.png")

    TextPerfectUntil = Image(path=sprite_path(r"ae95586e-1e38-45d1-8712-7553634cd627.png"), name="text_perfect_until.png")

    TextPleaseSelectPDrink = Image(path=sprite_path(r"dd305527-a69e-4241-9f95-6dafa84f115d.png"), name="text_please_select_p_drink.png")

    TextPDiary = Image(path=sprite_path(r"4c362a9a-9658-4f1b-bd87-a9e76a0a60cb.png"), name="text_p_diary.png")

    TextPDrinkMax = Image(path=sprite_path(r"dfd098de-4f80-40f5-a4bc-22ba7b1c1bc3.png"), name="text_p_drink_max.png")

    TextSenseiTipConsult = Image(path=sprite_path(r"704215cd-8a54-4a81-9ea2-6ba39978efd2.png"), name="text_sensei_tip_consult.png")

    TextSenseiTipDance = Image(path=sprite_path(r"0bd3a3dc-851f-4a22-9eb8-671d7c0fadce.png"), name="text_sensei_tip_dance.png")

    TextSenseiTipRest = Image(path=sprite_path(r"a0119583-b3cd-45ba-9aac-2a8da0f0c2dd.png"), name="text_sensei_tip_rest.png")

    TextSenseiTipVisual = Image(path=sprite_path(r"5ca24e09-b757-45a4-a36a-71d92b7b0a25.png"), name="text_sensei_tip_visual.png")

    TextSenseiTipVocal = Image(path=sprite_path(r"e739c0ef-3d47-413f-950b-07b3752894bd.png"), name="text_sensei_tip_vocal.png")

    TextSkipTurnDialog = Image(path=sprite_path(r"d5cd73c7-58c4-42e3-a7e1-93e7844bd125.png"), name="text_skip_turn_dialog.png")

    TextVisual = Image(path=sprite_path(r"f2bb9c44-42f5-47ee-b326-d88973c3b853.png"), name="text_visual.png")

    class Action:
        
        ActionStudy = Image(path=sprite_path(r"7df55226-1182-4421-bcaf-aeec4c758c66.png"), name="action_study.png")
    
        PDorinkuBg = Image(path=sprite_path(r"8748e1a6-a143-45f5-a9b1-1d5170909ba1.png"), name="p_dorinku_bg.png")
    
        PDorinkuBgMask = Image(path=sprite_path(r"d6b000e1-8525-4006-82fc-3164de903df8.png"), name="p_dorinku_bg_mask.png")
    
        PItem = Image(path=sprite_path(r"4315fbd6-888d-478e-bec8-596c13b2e031.png"), name="p_item.png")
    
        VocalWhiteBg = Image(path=sprite_path(r"4fa523ea-ac47-493d-9912-27e5c307a79a.png"), name="vocal_white_bg.png")
    
    
        pass

    pass
class Kuyo:
    
    ButtonStartGame = Image(path=sprite_path(r"3710f96c-22d4-441c-bb3b-d12e7cb3415c.png"), name="button_start_game.png")

    ButtonTab3Speedup = Image(path=sprite_path(r"e4af2462-a4c4-49da-b8f8-415827a3cb50.png"), name="button_tab3_speedup.png")


    pass